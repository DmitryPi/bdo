import json
import random

from datetime import datetime
from time import sleep
from threading import Thread, Lock
from enum import Enum, auto

from .bdo import Ability
from .keys import Keys
from .utils import get_datetime_passed_seconds, wind_mouse_move_camera, calc_rect_middle


class BotState(Enum):
    INIT = auto()
    SEARCHING = auto()
    NAVIGATING = auto()
    KILLING = auto()


class BlackDesertBot:
    # threading properties
    stopped = True
    lock = None
    # properties
    state = None
    screen = None
    targets = []
    buff_queue = []
    food_queue = []
    skill_queue = []
    ability_cooldowns = []
    main_loop_delay = 0.04

    def __init__(self):
        # create a thread lock object
        self.lock = Lock()

        # Abilities init
        self.buffs = self.load_abilities(ability_type='buff')
        self.foods = self.load_abilities(ability_type='food')
        self.heals = self.load_abilities(ability_type='heal')
        self.skills = self.load_abilities(ability_type='skill')
        # State and Keys init
        self.state = BotState.INIT
        self.keys = Keys()

    def load_abilities(self, ability_type='skill') -> list[Ability]:
        path = f'data/{ability_type}s.json'
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data = [Ability(*tuple(i.values())) for i in data]
            return data

    def camera_follow_target(self, rect: tuple) -> None:
        viewport_mp = (1920 / 2, 1080 / 3)
        x, y, w, h = calc_rect_middle(rect)
        move_x = int(x - viewport_mp[0])
        move_y = int(y - viewport_mp[1])
        if abs(move_x) < 50 and abs(move_y) < 50:
            return None
        overhead = 35
        move_x = move_x + overhead if move_x > 0 else move_x - overhead
        wind_mouse_move_camera(move_x, move_y)

    def filter_ability_cooldowns(self) -> None:
        """Filter by abilities by timestamp;
           Remove ability from cooldowns - delete_ability_cooldown"""
        for i, (ability, timestamp) in enumerate(self.ability_cooldowns):
            passed_sec = get_datetime_passed_seconds(timestamp)
            if passed_sec >= ability.cooldown:
                print('- OFF COOLDOWN', ability.name)
                self.delete_ability_cooldown(i)
                break

    def update_targets(self, targets: list[tuple]) -> None:
        """Threading method: update targets property"""
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screen(self, screen: object) -> None:
        """Threading method: update screen property"""
        self.lock.acquire()
        self.screen = screen
        self.lock.release()

    def update_ability_cooldowns(self, ability: tuple) -> None:
        """Threading method: update ability_cooldowns property"""
        self.lock.acquire()
        self.ability_cooldowns.append(ability)
        self.lock.release()

    def delete_ability_cooldown(self, index: int) -> None:
        """Threading method: delete ability_cooldown property"""
        self.lock.acquire()
        del self.ability_cooldowns[index]
        self.lock.release()

    def use_ability(self, ability: Ability, keybind=None) -> None:
        """Press/Release key sequence or hold and release after completing key sequence
           Supports keys and mouse(lmb/rmb)
           '+' is a suffix for key holding"""
        ability_cooldowns = [ability[0].name for ability in self.ability_cooldowns]  # names

        if ability.name in ability_cooldowns:
            print('- Ability cooldown:', ability.name)
            return None
        if ability.disabled:
            print('- Ability disabled:', ability.name)
            return None

        pressed = []
        rnd_press_range = (0.1, 0.25)
        print(f'- Using {ability.type}:', ability.name)
        for key in ability.keybind:
            try:
                sleep(key)
            except TypeError:
                hold = True if '+' in key else False
                key = key.replace('+', '')
                if 'lmb' in key:
                    self.keys.directMouse(buttons=self.keys.mouse_lb_press)
                    if not hold:
                        sleep(random.uniform(*rnd_press_range))
                        self.keys.directMouse(buttons=self.keys.mouse_lb_release)
                elif 'rmb' in key:
                    self.keys.directMouse(buttons=self.keys.mouse_rb_press)
                    if not hold:
                        sleep(random.uniform(*rnd_press_range))
                        self.keys.directMouse(buttons=self.keys.mouse_rb_release)
                else:
                    self.keys.directKey(key)
                    if not hold:
                        sleep(random.uniform(*rnd_press_range))
                        self.keys.directKey(key, self.keys.key_release)
                if hold:
                    pressed.append(key)
        # release keys/mouse
        for key in pressed:
            if 'lmb' in key:
                self.keys.directMouse(buttons=self.keys.mouse_lb_release)
            elif 'rmb' in key:
                self.keys.directMouse(buttons=self.keys.mouse_rb_release)
            else:
                self.keys.directKey(key, self.keys.key_release)
        sleep(ability.duration)
        # update ability_cooldowns
        self.update_ability_cooldowns((ability, str(datetime.now())))

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def set_state(self, state: BotState) -> None:
        print('\n- State changed:', state.name)
        self.state = state

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if self.state == BotState.INIT:
                self.set_state(BotState.SEARCHING)
            elif self.state == BotState.SEARCHING:
                if not self.targets:
                    # wind_mouse_move_camera(300, 0, delay=True)
                    pass
                else:
                    self.set_state(BotState.NAVIGATING)
            elif self.state == BotState.NAVIGATING:
                if not self.targets:
                    self.set_state(BotState.SEARCHING)
                    continue
                self.camera_follow_target(random.choice(self.targets))
                self.set_state(BotState.KILLING)
            elif self.state == BotState.KILLING:
                if not self.targets:
                    self.set_state(BotState.SEARCHING)
                    continue
                for skill in self.skills:
                    if not self.targets or self.stopped:
                        break
                    self.use_ability(skill)
            sleep(self.main_loop_delay)

import json
import random

from time import sleep
from threading import Thread, Lock
from enum import Enum, auto

from .bdo import Ability
from .keys import Keys


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
        x, y, w, h = rect
        move_x = int(x - viewport_mp[0])
        move_y = int(y - viewport_mp[1])
        if x > viewport_mp[0]:
            print('MORE', move_x)
        elif x < viewport_mp[0]:
            print('LESS', move_x)
        self.keys.directMouse(move_x, move_y)

    def move_to_target(self):
        pass

    def kill_target(self):
        pass

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

    def use_ability(self, ability: Ability, keybind=None) -> None:
        """Press/Release key sequence or hold and release after completing key sequence
           Supports keys and mouse(lmb/rmb)
           '+' is a suffix for key holding"""
        rnd_press_range = (0.1, 0.25)
        print(f'- Using {ability.type}:', ability.name)
        pressed = []
        for key in ability.keybind:
            try:
                sleep(key)
            except TypeError:
                print('- Pressing:', key)
                hold = True if '+' in key else False
                print(key, hold)
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
            if key in 'lmb':
                self.keys.directMouse(buttons=self.keys.mouse_rb_release)
            elif key in 'rmb':
                self.keys.directMouse(buttons=self.keys.mouse_lb_release)
            else:
                self.keys.directKey(key, self.keys.key_release)
        sleep(ability.duration)

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def set_state(self, state: BotState) -> None:
        print('- State changed:', state.name)
        self.state = state

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            print('- Inner loop working')
            if self.state == BotState.INIT:
                self.set_state(BotState.SEARCHING)
            elif self.state == BotState.SEARCHING:
                if not self.targets:
                    self.keys.directMouse(100, 0)
                    sleep(0.2)
                else:
                    self.set_state(BotState.NAVIGATING)
            elif self.state == BotState.NAVIGATING:
                if not self.targets:
                    self.set_state(BotState.SEARCHING)
                    continue
                self.camera_follow_target(self.targets[0])
                self.set_state(BotState.KILLING)
            elif self.state == BotState.KILLING:
                if not self.targets:
                    self.set_state(BotState.SEARCHING)
                    continue
                for skill in self.skills:
                    if not self.targets:
                        break
                    self.use_ability(skill)
            sleep(self.main_loop_delay)

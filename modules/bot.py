import json
import random

from datetime import datetime
from time import sleep
from threading import Thread, Lock
from enum import Enum, auto

from .bdo import Ability
from .keys import Keys
from .utils import get_datetime_passed_seconds


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
    character_position = []
    buff_queue = []  # when killing check buff icon; add to queue
    food_queue = []  # when killing check food icon; add to queue
    ability_cooldowns = []
    main_loop_delay = 0.04
    # constants
    INITIALIZING_SECONDS = 1

    def __init__(self, character='guard'):
        # create a thread lock object
        self.lock = Lock()

        # Abilities init
        self.buffs = self.load_abilities(ability_type=f'{character}_buff')
        self.foods = self.load_abilities(ability_type=f'{character}_food')
        self.heals = self.load_abilities(ability_type=f'{character}_heal')
        self.skills = self.load_abilities(ability_type=f'{character}_skill')
        self.dodges = self.load_abilities(ability_type=f'{character}_dodge')
        # State and Keys init
        self.state = BotState.INIT
        self.keys = Keys()

    def load_abilities(self, ability_type='skill') -> list[Ability]:
        path = f'data/{ability_type}s.json'
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data = [Ability(*tuple(i.values())) for i in data]
            return data

    def filter_ability_cooldowns(self) -> None:
        """Filter by abilities by timestamp;
           Remove ability from cooldowns - delete_ability_cooldown"""
        for i, (ability, timestamp) in enumerate(self.ability_cooldowns):
            passed_sec = get_datetime_passed_seconds(timestamp)
            if passed_sec >= ability.cooldown:
                # print('- OFF COOLDOWN', ability.name)
                self.delete_ability_cooldown(i)
                break

    def update_targets(self, targets: list[tuple]) -> None:
        """Threading method: update targets property"""
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_character_position(self, character_position: list[tuple]) -> None:
        """Threading method: update character_position property"""
        self.lock.acquire()
        self.character_position = character_position
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

    def dodge_back(self) -> None:
        """If target below character_position (behind character) - dodge back"""
        if self.character_position and self.targets:
            char_pos_y = self.character_position[0][1]
            # check if target_y below character_position_y
            targets_y = [i[1] for i in self.targets if char_pos_y < i[1]]
            if targets_y:
                self.use_ability(self.dodges[0])

    def use_ability(self, ability: Ability, keybind=None) -> None:
        """Press/Release key sequence or hold and release after completing key sequence
           Supports keys and mouse(lmb/rmb)
           '+' is a suffix for key holding"""
        ability_cooldowns = [ability[0].name for ability in self.ability_cooldowns]  # names

        if ability.name in ability_cooldowns:
            # print('- Ability cooldown:', ability.name)
            return None
        if ability.disabled:
            # print('- Ability disabled:', ability.name)
            return None

        pressed = []
        rnd_press_range = (0.1, 0.25)
        # update ability_cooldowns
        self.update_ability_cooldowns((ability, str(datetime.now())))
        # use ability
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

    def start(self) -> None:
        self.stopped = False
        t = Thread(target=self.run)
        t.start()
        print(f'- {__class__.__name__} started')

    def stop(self):
        self.stopped = True
        print(f'- {__class__.__name__} stopped')

    def set_state(self, state: BotState) -> None:
        print('\n- State changed:', state.name)
        self.state = state

    def run(self):
        while not self.stopped:
            if self.state == BotState.INIT:
                sleep(self.INITIALIZING_SECONDS)
                self.set_state(BotState.SEARCHING)
            elif self.state == BotState.SEARCHING:
                if not self.targets:
                    self.use_ability(self.skills[1])  # Всплеск Инферно
                else:
                    self.set_state(BotState.KILLING)
            elif self.state == BotState.NAVIGATING:
                pass
            elif self.state == BotState.KILLING:
                if not self.targets:
                    self.set_state(BotState.SEARCHING)
                    continue
                # self.dodge_back()
                self.use_ability(self.dodges[0])
                self.use_ability(random.choice(self.buffs))
                self.use_ability(self.skills[0])  # Доблестный Удар
                self.use_ability(random.choice(self.skills))
            sleep(self.main_loop_delay)

import cv2 as cv
import json
import random
import win32api

from datetime import datetime
from time import sleep
from threading import Thread, Lock
from enum import Enum, auto

from .bdo import Ability
from .vision import Vision
from .keys import Keys
from .utils import (
    press_btn,
    mouse_move_to,
    mouse_click_lb,
    mouse_click_rb,
    calc_rect_middle,
    get_datetime_passed_seconds,
    send_telegram_msg,
)


class BotState(Enum):
    INIT = auto()
    SEARCHING = auto()
    KILLING = auto()


class BotBuffer:
    # constants
    INITIALIZING_SECONDS = 0.5
    # threading properties
    stopped = True
    lock = None
    # properties
    screen = None
    buff_queue = []
    main_loop_delay = 0.3

    def __init__(self, buffs: list[Ability]):
        # create a thread lock object
        self.lock = Lock()
        # properties
        self.buffs = buffs
        self.vision = Vision()

    def search_for_buffs(self) -> None:
        """Find buff/food icons in cropped areas; update buff_queue"""
        found_buffs = []
        for buff in self.buffs:
            if buff.disabled:
                continue
            if buff.type == 'buff':
                result = self.search_buff(buff, crop=[1440, 580, 1900, 925])
                if result:  # check if buff found
                    found_buffs.append(buff)
            elif buff.type == 'food':
                result = self.search_buff(buff, crop=[820, 960, 1370, 1050])
                if not result:  # check if food not found
                    found_buffs.append(buff)
        self.buff_queue = found_buffs  # replace buff_queue

    def search_buff(self, buff: Ability, crop=[]) -> list[Ability]:
        """cv2 search buff/food icon"""
        needle_img = buff.icon[0]
        threshold = buff.icon[1]
        result = self.vision.find(self.screen, needle_img, threshold=threshold, crop=crop)
        return result

    def update_screen(self, screen: object) -> None:
        """Threading method: update screen property"""
        self.lock.acquire()
        self.screen = screen
        self.lock.release()

    def start(self) -> None:
        self.stopped = False
        t = Thread(target=self.run)
        t.start()
        print(f'- {__class__.__name__} started')

    def stop(self):
        self.stopped = True
        print(f'- {__class__.__name__} stopped')

    def run(self):
        sleep(self.INITIALIZING_SECONDS)
        while not self.stopped:
            self.search_for_buffs()
            sleep(self.main_loop_delay)


class BlackDesertBot:
    # constants
    INITIALIZING_SECONDS = 1
    # threading properties
    stopped = True
    lock = None
    # properties
    state = None
    screen = None
    targets = []
    character_position = []
    buff_queue = []  # when killing check buff icon; add to queue
    ability_cooldowns = []
    main_loop_delay = 0.04
    rnd_press_range = (0.1, 0.25)

    def __init__(self, character='guard'):
        # create a thread lock object
        self.lock = Lock()
        # Abilities init
        self.buffs = self.load_abilities(ability_type=f'{character}_buff')
        self.foods = self.load_abilities(ability_type=f'{character}_food')
        self.heals = self.load_abilities(ability_type=f'{character}_heal')
        self.skills = self.load_abilities(ability_type=f'{character}_skill')
        self.dodges = self.load_abilities(ability_type=f'{character}_dodge')
        # state
        self.state = BotState.INIT
        # properties
        self.keys = Keys()
        self.vision = Vision()

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

    def update_buff_queue(self, buff_queue: list[Ability]) -> None:
        """Threading method: update buff_queue property"""
        self.lock.acquire()
        self.buff_queue = buff_queue
        self.lock.release()

    def delete_ability_cooldown(self, index: int) -> None:
        """Threading method: delete ability_cooldown property"""
        self.lock.acquire()
        del self.ability_cooldowns[index]
        self.lock.release()

    def use_dodge_back(self, dodge: Ability) -> None:
        """If target below character_position (behind character) - dodge back"""
        if self.targets:
            pos_y = 685  # check if target_y below character_position_y
            targets_y = [i for i in self.targets if pos_y < i[1]]
            if len(targets_y) >= 2:
                self.use_ability(dodge)

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
        # update ability_cooldowns
        self.update_ability_cooldowns((ability, str(datetime.now())))
        # use ability
        # print(f'- Using {ability.type}:', ability.name)
        for key in ability.keybind:
            try:
                sleep(key)
            except TypeError:
                hold = True if '+' in key else False
                key = key.replace('+', '')
                if 'lmb' in key:
                    self.keys.directMouse(buttons=self.keys.mouse_lb_press)
                    if not hold:
                        sleep(random.uniform(*self.rnd_press_range))
                        self.keys.directMouse(buttons=self.keys.mouse_lb_release)
                elif 'rmb' in key:
                    self.keys.directMouse(buttons=self.keys.mouse_rb_press)
                    if not hold:
                        sleep(random.uniform(*self.rnd_press_range))
                        self.keys.directMouse(buttons=self.keys.mouse_rb_release)
                else:
                    self.keys.directKey(key)
                    if not hold:
                        sleep(random.uniform(*self.rnd_press_range))
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

    def open_ui(self, ui: str) -> None:
        result = self.vision.find_ui(self.screen, ui, onlyone=True)
        mouse_move_to(result[0], result[1])
        mouse_click_lb()

    def maid_chest_manage(self) -> bool:
        """Open maid chest => put loot items into it"""
        try:
            find_ui = self.vision.find_ui
            inventory_opened = find_ui(self.screen, 'inventory_opened')
            chest_opened = find_ui(self.screen, 'chest_opened')

            if not inventory_opened:  # show cursor
                press_btn('i')

            if chest_opened:
                print('- Chest Opened')
                # self.maid_chest_put_loot()
                return True
            else:
                maid_opened = find_ui(self.screen, 'maid_opened')
                if maid_opened:
                    self.open_ui('maid_chest_open')
                else:
                    self.open_ui('maid_open')
        except (ValueError, IndexError) as e:
            print(e)

    def maid_chest_put_loot(self) -> bool:
        """Put loot items to maid stash"""
        items = self.vision.find_loot(self.screen)
        for item in items:
            mouse_move_to(item[0], item[1])
            sleep(0.3)
            mouse_click_rb()
            sleep(0.5)
            press_btn('space')

    def camp_repair_manage(self) -> bool:
        find_ui = self.vision.find_ui
        try:
            # run to camp
            if find_ui(self.screen, 'camp_toofar'):
                self.camp_run_to()
            # repair confirm
            if self.camp_repair_confirm():
                print('- Repair successful')
                return True
            # if not inventory opened - cursor not shown
            if not find_ui(self.screen, 'inventory_opened'):
                press_btn('i')  # will show cursor
            # open camp menu
            if find_ui(self.screen, 'camp_opened'):
                # click repair btn
                result = find_ui(self.screen, 'camp_repair', onlyone=True)
                mouse_move_to(result[0], result[1])
                mouse_click_lb()
            else:
                result = find_ui(self.screen, 'camp_open', onlyone=True)
                mouse_move_to(result[0], result[1])
                mouse_click_lb()
        except (ValueError, IndexError) as e:
            print(e)

    def camp_run_to(self):
        print('- Run to camp')
        press_btn('t')
        sleep(5)
        mouse_click_lb()

    def camp_repair_confirm(self) -> bool:
        result = self.vision.find_ui(self.screen, 'camp_repair_confirm', onlyone=True)
        if result:
            mouse_move_to(result[0], result[1])
            mouse_click_lb()
            sleep(0.4)
            press_btn('space')
            press_btn('esc')
            press_btn('esc')
            return True

    def set_state(self, state: BotState) -> None:
        print('\n- State changed:', state.name)
        self.state = state

    def start(self) -> None:
        self.stopped = False
        t = Thread(target=self.run)
        t.start()
        print(f'- {__class__.__name__} started')

    def stop(self):
        self.stopped = True
        print(f'- {__class__.__name__} stopped')

    def run(self):
        telegram_msg_sent = False
        i = 0
        while not self.stopped:
            if self.state == BotState.INIT:
                sleep(self.INITIALIZING_SECONDS)
                self.set_state(BotState.SEARCHING)
            elif self.state == BotState.SEARCHING:
                if not self.targets:
                    i += 1
                    self.use_ability(self.skills[1])  # Всплеск Инферно
                    if i >= 200:
                        if not telegram_msg_sent:
                            screen_path = 'assets/last_screen.jpg'
                            cv.imwrite(screen_path, cv.cvtColor(self.screen, cv.COLOR_BGR2RGB))
                            send_telegram_msg('\nCant find target', photo_path=screen_path)
                        telegram_msg_sent = True
                        sleep(15)
                else:
                    i = 0
                    telegram_msg_sent = False
                    self.set_state(BotState.KILLING)
            elif self.state == BotState.KILLING:
                if not self.targets:
                    self.set_state(BotState.SEARCHING)
                    continue
                if self.buff_queue:
                    self.use_ability(random.choice(self.buff_queue))
                self.use_ability(random.choice(self.dodges))  # same name Уклонение
                self.use_ability(self.skills[0])  # Доблестный Удар
                self.use_ability(random.choice(self.skills))
            sleep(self.main_loop_delay)

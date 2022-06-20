import cv2 as cv
import json
import random

from time import sleep
from enum import Enum, auto

from .bdo import Ability
from .keys import Keys
from .utils import grab_screen
from .vision import Vision, WindowCapture


class BotState(Enum):
    INIT = auto()
    SEARCHING = auto()
    NAVIGATING = auto()
    KILLING = auto()


class BlackDesertBot:
    state = None
    buff_queue = []
    food_queue = []
    skill_queue = []
    # threading properties
    stopped = True
    lock = None

    def __init__(self):
        self.state = BotState.INIT
        self.keys = Keys()
        self.buffs = self.load_abilities(ability_type='buff')
        self.foods = self.load_abilities(ability_type='food')
        self.skills = self.load_abilities(ability_type='skill')

    def load_abilities(self, ability_type='skill') -> list[Ability]:
        path = f'data/{ability_type}s.json'
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data = [Ability(*tuple(i.values())) for i in data]
            return data

    def find_target(self, tmplt):
        while True:
            screen = grab_screen(region=(-1920, 350, 0, 1430))
            screen = cv.cvtColor(screen, cv.COLOR_BGR2RGB)

            screen = cv.resize(screen, (960, 540))
            cv.imshow('screen', screen)

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

    def follow_target(self):
        pass

    def move_to_target(self):
        pass

    def kill_target(self):
        pass

    def use_buff(self):
        pass

    def use_food(self):
        pass

    def use_skill(self, keybind=None) -> None:
        """Press/Release key sequence or hold and release after completing key sequence
           Supports keys and mouse(lmb/rmb)"""
        rnd_press_range = (0.1, 0.25)
        for skill in self.skills:
            print('- Using Skill:', skill.name)
            pressed = []
            for key in skill.keybind:
                try:
                    sleep(key)
                except TypeError:
                    print('- Pressing:', key)
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
                if key in 'lmb':
                    self.keys.directMouse(buttons=self.keys.mouse_rb_release)
                elif key in 'rmb':
                    self.keys.directMouse(buttons=self.keys.mouse_lb_release)
                else:
                    self.keys.directKey(key, self.keys.key_release)
            sleep(skill.duration)

    def run(self):
        pass

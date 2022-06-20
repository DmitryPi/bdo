from enum import Enum, auto

from .bdo import Ability
from .utils import grab_screen


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
        self.buffs = []
        self.food = []
        self.skills = []

    def load_abilities(self, type='skill'):
        pass

    def find_target(self):
        pass

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

    def use_skill(self):
        pass

    def run(self):
        pass

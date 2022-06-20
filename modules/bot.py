from enum import Enum

from bdo import Ability
from utils import grab_screen


class BotState(Enum):
    INIT = 'INIT'
    SEARCHING = 'SEARCHING'
    NAVIGATING = 'NAVIGATING'
    KILLING = 'KILLING'


class BlackDesertBot:
    def __init__(self):
        pass

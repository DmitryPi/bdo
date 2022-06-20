from enum import Enum
from dataclasses import dataclass


class AbilityType(Enum):
    BUFF = 'buff'
    FOOD = 'food'
    SKILL = 'skill'


@dataclass(frozen=True)
class Ability:
    name: str
    keybind: str
    type: AbilityType
    icon: str = ''
    duration: int = 0
    disabled: bool = False

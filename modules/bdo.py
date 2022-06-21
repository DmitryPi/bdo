from enum import Enum
from dataclasses import dataclass


class AbilityType(Enum):
    BUFF = 'buff'
    FOOD = 'food'
    HEAL = 'heal'
    SKILL = 'skill'


@dataclass(frozen=True)
class Ability:
    name: str
    keybind: list[str]
    type: AbilityType
    icon: str = ''
    cooldown: int = 0
    duration: int = 0
    disabled: bool = False

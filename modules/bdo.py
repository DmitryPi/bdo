from enum import Enum
from dataclasses import dataclass, field


class AbilityType(Enum):
    SKILL = 'skill'
    BUFF = 'buff'
    FOOD = 'food'


@dataclass(frozen=True)
class Ability:
    name: str
    keybind: str
    type: AbilityType
    icon: str = ''
    duration: int = 0
    disabled: bool = False


if __name__ == '__main__':
    skill_1 = Ability('E buff', 'e', AbilityType('buff').value)
    skill_2 = Ability('Lunacy', 'ctrl+e', AbilityType.SKILL.value)
    print(skill_1)
    print(skill_2)

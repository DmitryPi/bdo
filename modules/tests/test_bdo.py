from unittest import TestCase

from modules.bdo import Ability, AbilityType


class TestAbilityType(TestCase):
    def setUp(self):
        self.type_1 = AbilityType('buff')
        self.type_2 = AbilityType('food')
        self.type_3 = AbilityType('skill')

    def test_types(self):
        self.assertTrue(self.type_1.value == 'buff')
        self.assertTrue(isinstance(self.type_1, AbilityType))
        self.assertTrue(self.type_2.value == 'food')
        self.assertTrue(isinstance(self.type_2, AbilityType))
        self.assertTrue(self.type_3.value == 'skill')
        self.assertTrue(isinstance(self.type_3, AbilityType))


class TestAbility(TestCase):
    def setUp(self):
        self.type_1 = AbilityType('buff')
        self.type_2 = AbilityType('food')
        self.type_3 = AbilityType('skill')
        self.ability_1 = Ability('Buff', 'e', self.type_1.value)
        self.ability_2 = Ability('Food', '1', self.type_2.value, disabled=True)
        self.ability_3 = Ability('Skill', 'ctrl+e', self.type_3.value)

    def test_abilities(self):
        # 1
        assert self.ability_1.name == 'Buff'
        assert self.ability_1.keybind == 'e'
        assert self.ability_1.type == 'buff'
        assert not self.ability_1.disabled
        # 2
        assert self.ability_2.name == 'Food'
        assert self.ability_2.keybind == '1'
        assert self.ability_2.type == 'food'
        assert self.ability_2.disabled
        # 3
        assert self.ability_3.name == 'Skill'
        assert self.ability_3.keybind == 'ctrl+e'
        assert self.ability_3.type == 'skill'
        assert not self.ability_3.disabled

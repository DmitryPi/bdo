import pytest

from unittest import TestCase

from ..bdo import Ability
from ..bot import BotState, BlackDesertBot


class TestBotState(TestCase):
    def setUp(self):
        self.state_1 = BotState.INIT
        self.state_2 = BotState.SEARCHING
        self.state_3 = BotState.NAVIGATING
        self.state_4 = BotState.KILLING

    def test_types(self):
        assert self.state_1.name == 'INIT'
        assert isinstance(self.state_1, BotState)
        assert self.state_2.name == 'SEARCHING'
        assert isinstance(self.state_2, BotState)
        assert self.state_3.name == 'NAVIGATING'
        assert isinstance(self.state_3, BotState)
        assert self.state_4.name == 'KILLING'
        assert isinstance(self.state_4, BotState)


class TestBlackDesertBot(TestCase):
    def setUp(self):
        self.bot = BlackDesertBot()

    def test_state(self):
        assert self.bot.state == BotState.INIT

    def test_load_abilities(self):
        buffs = self.bot.load_abilities(ability_type='buff')
        foods = self.bot.load_abilities(ability_type='food')
        skills = self.bot.load_abilities(ability_type='skill')
        assert isinstance(buffs, list)
        assert isinstance(foods, list)
        assert isinstance(skills, list)
        assert isinstance(self.bot.buffs[0], Ability)
        assert isinstance(self.bot.foods[0], Ability)
        assert isinstance(self.bot.skills[0], Ability)

    @pytest.mark.slow
    def test_use_ability(self):
        for skill in self.bot.skills:
            self.bot.use_ability(skill)

    def test_filter_ability_cooldowns(self):
        ability_cooldowns = [
            ('Проекция', 15, '2022-06-22 00:33:51.202546'),
            ('Лавовое Озеро', 15, '2022-06-22 00:33:51.954306'),
            ('Огненная Ярость', 6, '2022-06-22 00:33:53.622277'),
            ('Очаг Пожара', 6, '2022-06-22 00:33:54.895727'),
            ('Водоворот', 6, '2022-06-22 00:34:00.327718')]
        self.bot.ability_cooldowns = ability_cooldowns
        self.bot.filter_ability_cooldowns()
        self.bot.filter_ability_cooldowns()
        self.bot.filter_ability_cooldowns()
        self.bot.filter_ability_cooldowns()
        self.bot.filter_ability_cooldowns()
        assert not self.bot.ability_cooldowns

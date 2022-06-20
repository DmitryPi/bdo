from unittest import TestCase

from modules.bot import BotState, BlackDesertBot


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

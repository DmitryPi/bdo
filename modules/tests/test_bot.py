from unittest import TestCase


from modules.bot import BotState


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

import pytest

from time import sleep
from unittest import TestCase

from ..keys import Keys
from ..utils import wind_mouse_move_camera


class TestUtils(TestCase):
    def setUp(self):
        self.keys = Keys()

    @pytest.mark.slow
    def test_wind_mouse_move_camera(self):
        movements = [
            (2000, 0)]
        sleep(1)
        for (x, y) in movements:
            wind_mouse_move_camera(x, y, step=40)

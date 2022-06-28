import pytest
import win32api

from time import sleep
from unittest import TestCase

from ..keys import Keys
from ..utils import wind_mouse, wind_mouse_move_camera


class TestUtils(TestCase):
    def setUp(self):
        self.keys = Keys()

    @pytest.mark.slow
    def test_wind_mouse_move_camera(self):
        movements = [
            (500, 0)]
        sleep(3)
        for (x, y) in movements:
            wind_mouse_move_camera(x, y, step=30)
            wind_mouse_move_camera(x, y, step=30)
            wind_mouse_move_camera(x, y, step=30)

    @pytest.mark.slow
    def test_wind_mouse(self):
        sleep(3)
        move_func = win32api.SetCursorPos
        step = 30
        pos_x, pos_y = win32api.GetCursorPos()
        wind_mouse(pos_x, pos_y, 1920, pos_y, M_0=step, D_0=step, move_mouse=move_func, delay=True)
        pos_x, pos_y = win32api.GetCursorPos()
        wind_mouse(pos_x, pos_y, 1000, pos_y, M_0=step, D_0=step, move_mouse=move_func, delay=True)

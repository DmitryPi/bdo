import pytest

from unittest import TestCase

from ..utils import grab_screen
from ..vision import Vision


class TestVision(TestCase):
    def setUp(self):
        self.vision = Vision()
        self.screen = grab_screen(region=(0, 0, 1920, 1080))

    def test_cvt_img_gray(self):
        screen_gray = self.vision.cvt_img_gray(self.screen)
        assert isinstance(screen_gray, object)
        assert isinstance(screen_gray, object)

    def test_find(self):
        self.vision.find_ui(self.screen, 'vessel')

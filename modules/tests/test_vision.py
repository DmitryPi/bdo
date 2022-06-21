import pytest

from unittest import TestCase

from ..utils import grab_screen
from ..vision import Vision


class TestVision(TestCase):
    def setUp(self):
        self.vision = Vision('assets/boar.png')
        self.screen = grab_screen(region=(0, 0, 1920, 1080))

    def test_vision_init(self):
        assert isinstance(self.vision.needle_img, object)
        assert isinstance(self.vision.needle_w, int)
        assert isinstance(self.vision.needle_h, int)

    def test_cvt_img_gray(self):
        screen_gray = self.vision.cvt_img_gray(self.screen)
        assert isinstance(screen_gray, object)
        assert isinstance(screen_gray, object)

    def test_match_template(self):
        screen_gray = self.vision.cvt_img_gray(self.screen)
        locations = self.vision.match_template(self.vision.needle_img, screen_gray, threshold=0.9)
        assert not locations

    def test_find(self):
        self.vision.find(self.screen, crop=[0, 0, 500, 500], threshold=0.15)

import cv2 as cv
import pytest

from unittest import TestCase

from ..utils import grab_screen
from ..vision import Vision


class TestVision(TestCase):
    def setUp(self):
        self.vision = Vision('assets/boar.png')
        self.vision.debug = True

    def test_vision_init(self):
        assert isinstance(self.vision.needle_img, object)
        assert isinstance(self.vision.needle_w, int)
        assert isinstance(self.vision.needle_h, int)

    def test_cvt_img_gray(self):
        screen = grab_screen()
        screen_gray = self.vision.cvt_img_gray(screen)
        assert isinstance(screen_gray, object)
        assert isinstance(screen_gray, object)

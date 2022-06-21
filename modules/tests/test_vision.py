import pytest

from unittest import TestCase

from ..vision import Vision


class TestVision(TestCase):
    def setUp(self):
        pass

    def test_vision_init(self):
        vision = Vision('assets/boar.png')
        assert len(vision.needle_img)
        assert isinstance(vision.needle_w, int)
        assert isinstance(vision.needle_h, int)

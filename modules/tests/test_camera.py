import pytest

from unittest import TestCase

from ..camera import Camera
from ..vision import Vision


class TestCamera(TestCase):
    def setUp(self):
        self.camera = Camera(Vision('assets/character.png'))

    def test_choose_target(self):
        targets_0 = [(606, 0)]
        targets_1 = [(606, 0), (906, 0)]
        targets_2 = [(606, 0), (906, 0), (1206, 0)]
        targets_3 = [(606, 0), (906, 0), (1206, 0), (1215, 0), (1245, 0), (1276, 0)]
        targets_4 = [(606, 0), (906, 0), (1206, 0), (1215, 0), (1245, 0), (1276, 0), (1300, 0)]
        assert self.camera.choose_target(targets_0)[0] == 606
        assert self.camera.choose_target(targets_1)[0] == 606
        assert self.camera.choose_target(targets_2)[0] == 906
        assert self.camera.choose_target(targets_3)[0] == 1206
        assert self.camera.choose_target(targets_4)[0] == 1215

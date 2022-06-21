import cv2 as cv
import numpy as np

from time import time

from .utils import grab_screen


class Vision:
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.needle_img, self.needle_w, self.needle_h = self.process_img(needle_img_path)

    def process_img(self, img_path: str) -> tuple:
        """CV imread from path and return (img, width, height)"""
        img = cv.imread(img_path, 0)
        w, h = img.shape[::-1]
        return (img, w, h)

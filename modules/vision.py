import cv2 as cv
import numpy as np
import inspect

from time import time

from .utils import grab_screen


class Vision:
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.debug = False
        self.method = method
        self.needle_img, self.needle_w, self.needle_h = self.process_img(needle_img_path)

    def debug_imshow(self, funcname: str, img: object) -> None:
        """Show cv2 image if debug=True"""
        if not self.debug:
            return
        img = cv.resize(img, (960, 540))
        cv.imshow(funcname, img)
        cv.waitKey(500)

    def process_img(self, img_path: str) -> tuple:
        """CV imread from path and return (img, width, height)"""
        img = cv.imread(img_path, 0)
        w, h = img.shape[::-1]
        return (img, w, h)

    def cvt_img_gray(self, img: object, region=None) -> object:
        """cv2 convert image to gray"""
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        self.debug_imshow(inspect.stack()[0][3], img_gray)
        return img_gray

    def match_template(self, haystack: object, needle: object, threshold=0.65):
        """cv2 match template and return locations according to threshold"""
        result = cv.matchTemplate(haystack, needle, self.method)
        locations = np.where(result >= threshold)
        return locations

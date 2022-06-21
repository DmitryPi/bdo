import cv2 as cv
import numpy as np

from time import time

from .utils import grab_screen


class Vision:
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.method = method
        self.needle_img, self.needle_w, self.needle_h = self.process_img(needle_img_path)

    def debug_imshow(self, img: object) -> None:
        """Show cv2 image if debug=True"""
        if not self.debug:
            return
        img = cv.resize(img, (960, 540))
        cv.imshow('IMAGE', img)
        cv.waitKey(500)

    def process_img(self, img_path: str) -> tuple:
        """CV imread from path and return (img, width, height)"""
        img = cv.imread(img_path, 0)
        w, h = img.shape[::-1]
        return (img, w, h)

    def cvt_img_gray(self, img: object) -> object:
        """cv2 convert image to gray"""
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return img_gray

    def match_template(self, haystack: object, needle: object, threshold=0.65) -> list:
        """cv2 match template and return locations according to threshold"""
        result = cv.matchTemplate(haystack, needle, self.method)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))  # remove empty arrays
        return locations

    def find(self, screen: object, threshold=0.65, calc_mp=False, crop=[], debug=False) -> list[tuple]:
        """Find grayscaled object on screen by given threshold
           calc_mp - calculate needle middle points on screen
           crop - [x1, y1, x2, y2], screen region crop
           debug - show screen/screen_gray image"""
        screen_gray = self.cvt_img_gray(screen)

        if crop:
            screen = screen[crop[1]:crop[3], crop[0]:crop[2]]  # y1:y2, x1:x2
            screen_gray = screen_gray[crop[1]:crop[3], crop[0]:crop[2]]  # y1:y2, x1:x2

        # debug imshow
        if debug:
            self.debug_imshow(screen)
            self.debug_imshow(screen_gray)

        # find matches
        locations = self.match_template(screen_gray, self.needle_img, threshold=threshold)
        mask = np.zeros(screen.shape[:2], np.uint8)
        detected_objects = []

        for (x, y) in locations:
            if mask[y + self.needle_h // 2, x + self.needle_w // 2] != 255:
                if calc_mp:  # calculate object middle points
                    x_mp = int((x * 2 + self.needle_w) / 2)
                    y_mp = int((y * 2 + self.needle_h) / 2)
                    detected_objects.append((x_mp, y_mp))
                else:  # append detected object
                    detected_objects.append((x, y))
            # mask out detected object
            mask[y:y + self.needle_h, y:y + self.needle_w] = 255

        if crop:  # recalculate cropped region points
            for i, (x, y) in enumerate(detected_objects):
                detected_objects[i] = (x + crop[0], y + crop[1])

        return detected_objects

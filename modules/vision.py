import cv2 as cv
import numpy as np

from time import time

from .utils import grab_screen


class Vision:
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.method = method
        self.needle_img, self.needle_w, self.needle_h = self.process_img(needle_img_path)

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

    def find(self, screen: object, threshold=0.65, crop=[], debug=False) -> list[tuple]:
        """Find grayscaled object on screen by given threshold
           crop - [x1, y1, x2, y2], screen region crop
           debug - show screen/screen_gray image"""
        screen_gray = self.cvt_img_gray(screen)

        if crop:
            screen = screen[crop[1]:crop[3], crop[0]:crop[2]]  # y1:y2, x1:x2
            screen_gray = screen_gray[crop[1]:crop[3], crop[0]:crop[2]]  # y1:y2, x1:x2

        # find matches
        locations = self.match_template(screen_gray, self.needle_img, threshold=threshold)
        mask = np.zeros(screen.shape[:2], np.uint8)
        detected_objects = []

        for (x, y) in locations:
            if mask[y + self.needle_h // 2, x + self.needle_w // 2] != 255:
                detected_objects.append((x, y, self.needle_w, self.needle_h))
            mask[y:y + self.needle_h, y:y + self.needle_w] = 255  # mask out detected object

        if crop:  # recalculate cropped region points
            for i, (x, y, w, h) in enumerate(detected_objects):
                detected_objects[i] = (x + crop[0], y + crop[1], w, h)

        return detected_objects

    def calc_rect_middle(self, rect: tuple[int]) -> tuple[int]:
        """Calculate middle point of rectangle"""
        x, y, w, h = rect
        x = int((x * 2 + w) / 2)
        y = int((y * 2 + h) / 2)
        return (x, y, w, h)

    def draw_rectangles(self, haystack_img, rectangles):
        """given a list of [x, y, w, h] rectangles and a canvas image to draw on
           return an image with all of those rectangles drawn"""
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img

    def draw_crosshairs(self, haystack_img, points):
        """given a list of [x, y] positions and a canvas image to draw on
           return an image with all of those click points drawn on as crosshairs"""
        # these colors are actually BGR
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            # draw the center point
            cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img

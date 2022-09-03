import os
import cv2 as cv
import numpy as np


class Vision:
    def __init__(self, method=cv.TM_CCOEFF_NORMED):
        self.method = method

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

    def find(self, needle_img_path: str, screen: object, threshold=0.65, crop=[]) -> list[list[int]]:
        """Find grayscaled object on screen by given threshold
           crop - [x1, y1, x2, y2], screen region crop"""
        needle_img, needle_w, needle_h = self.process_img(needle_img_path)
        screen_gray = self.cvt_img_gray(screen)

        if crop:
            screen = screen[crop[1]:crop[3], crop[0]:crop[2]]  # y1:y2, x1:x2
            screen_gray = screen_gray[crop[1]:crop[3], crop[0]:crop[2]]  # y1:y2, x1:x2

        # find matches
        locations = self.match_template(screen_gray, needle_img, threshold=threshold)
        mask = np.zeros(screen.shape[:2], np.uint8)
        detected_objects = []

        for (x, y) in locations:
            if mask[y + needle_h // 2, x + needle_w // 2] != 255:
                detected_objects.append([x, y, needle_w, needle_h])
            mask[y:y + needle_h, x:x + needle_w] = 255  # mask out detected object

        if crop:  # recalculate cropped region points
            for i, (x, y, w, h) in enumerate(detected_objects):
                detected_objects[i] = [x + crop[0], y + crop[1], w, h]

        return detected_objects

    def find_character(self, screen: object, threshold=0.8, crop=[]) -> list[list[int]]:
        needle_img_path = 'assets/character.png'
        result = self.find(needle_img_path, screen, threshold=threshold, crop=crop)
        return result

    def find_kzarka(self, screen: object, threshold=0.75, crop=[450, 210, 1585, 930]) -> list[list[int]]:
        needle_img_path = 'assets/kzarka.png'
        result = self.find(needle_img_path, screen, threshold=threshold, crop=crop)
        return result

    def find_vessel(self, screen: object, threshold=0.62, crop=[0, 0, 1900, 500]) -> list[list[int]]:
        needle_img_path = 'assets/vessel.png'
        result = self.find(needle_img_path, screen, threshold=threshold, crop=crop)
        return result

    def find_weight_limit(
            self, screen: object, threshold=0.68, crop=[1335, 195, 1390, 240]) -> list[list[int]]:
        needle_img_path = 'assets/ui/weight_limit.png'
        result = self.find(needle_img_path, screen, threshold=threshold, crop=crop)
        return result

    def find_durability(
            self, screen: object, threshold=0.8, crop=[1530, 150, 1600, 200]) -> list[list[int]]:
        needle_img_path = 'assets/ui/armor_durability.png'
        result = self.find(needle_img_path, screen, threshold=threshold, crop=crop)
        return result

    def find_inventory(
            self, screen: object, threshold=0.8, crop=[928, 130, 1690, 200]) -> list[list[int]]:
        needle_img_path = 'assets/ui/inventory.png'
        result = self.find(needle_img_path, screen, threshold=threshold, crop=crop)
        return result

    def find_chest(
            self, screen: object, threshold=0.8, crop=[928, 130, 1690, 200]) -> list[list[int]]:
        needle_img_path = 'assets/ui/chest.png'
        result = self.find(needle_img_path, screen, threshold=threshold, crop=crop)
        return result

    def find_camp(
            self, screen: object, threshold=0.8, crop=[15, 170, 1435, 830]) -> list[list[int]]:
        needle_img_path = 'assets/ui/camp.png'
        result = self.find(needle_img_path, screen, threshold=threshold, crop=crop)
        return result

    def find_loot(
            self, screen: object, threshold=0.85, crop=[1460, 400, 1900, 745]) -> list[list[int]]:
        end_result = []
        for i in range(99):
            needle_img_path = f'assets/loot/{i}.png'
            if not os.path.exists(needle_img_path):
                break
            result = self.find(needle_img_path, screen, threshold=threshold, crop=crop)
            end_result += result
        return end_result

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

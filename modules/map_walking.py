import cv2
import numpy as np
import time

from keys import Keys
from utils import grab_screen


keys = Keys()
screen_sm = (-1920, 360, 0, 1440)
screen_lg = (0, 0, 2560, 1440)


def pathing(minimap):
    # lower = np.array([110, 100, 80])
    # upper = np.array([118, 150, 255])
    lower = np.array([0, 0, 0])
    upper = np.array([255, 255, 255])

    hsv = cv2.cvtColor(minimap, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(minimap, lower, upper)

    matches = np.argwhere(mask == 0)
    mean_y = np.mean(matches[:, 1])
    target = minimap.shape[1] / 2
    error = target - mean_y
    print(error)

    # keys.directMouse(-1 * int(error * 3), 0)

    cv2.imshow('Minimap', mask)
    cv2.waitKey(10)


# time.sleep(3)
# keys.directKey('w')

for i in range(20):
    screen = grab_screen(region=screen_sm)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    # minimap = screen[30:290, -330:-30]  # y1:y2 x1:x2
    # minimap = screen[30:500, -500:-30]  # y1:y2 x1:x2
    # miniminimap = screen[200:350, -325:-188]
    arrow_path = screen[260:480, -1075:-845]

    pathing(arrow_path)

    # screen = cv2.resize(screen, (960, 540))
    # cv2.imshow('screen', screen)
    # cv2.waitKey(10)
# keys.directKey('w', keys.key_release)
cv2.destroyAllWindows()

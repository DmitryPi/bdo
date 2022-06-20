import cv2
import numpy as np

from time import time, sleep
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


# sleep(3)
# keys.directKey('w')
loop_time = time()
frame_count = 0
previous_frame = None
while True:
    frame_count += 1

    screen = grab_screen(region=screen_sm)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

    if ((frame_count % 2) == 0):
        prepared_frame = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5, 5), sigmaX=0)

        # 3. Set previous frame and continue if there is None
        if (previous_frame is None):
            # First frame; there is no previous one yet
            previous_frame = prepared_frame
            continue

        # calculate difference and update previous frame
        diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
        previous_frame = prepared_frame

        # 4. Dilute the image a bit to make differences more seeable; more suitable for contour detection
        kernel = np.ones((5, 5))
        diff_frame = cv2.dilate(diff_frame, kernel, 1)

        # 5. Only take different areas that are different enough (>20 / 255)
        thresh_frame = cv2.threshold(src=diff_frame, thresh=5, maxval=255, type=cv2.THRESH_BINARY)[1]

        contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 1000:  # filter out small ones
                # too small: skip!
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(img=screen, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)

    screen = cv2.resize(screen, (960, 540))
    cv2.imshow('screen', screen)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
# keys.directKey('w', keys.key_release)
cv2.destroyAllWindows()

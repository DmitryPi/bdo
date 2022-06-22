import random

from time import sleep
from threading import Thread, Lock

from .vision import Vision
from .utils import wind_mouse_move_camera, calc_rect_middle


class Camera:
    """Manage ingame bot camera by giving Vision character object"""
    # threading properties
    stopped = True
    lock = None
    # properties
    state = None
    screen = None
    targets = []
    character_position = []
    main_loop_delay = 0.04
    # constants
    INITIALIZING_SECONDS = 1

    def __init__(self, character: Vision):
        # create a thread lock object
        self.character = character
        self.lock = Lock()

    def follow_target(self, rect: tuple) -> None:
        """Camera follow given target coords"""
        viewport_mp = (1920 / 2, 1080 / 3)
        x, y, w, h = calc_rect_middle(rect)
        move_x = int(x - viewport_mp[0])
        move_y = int(y - viewport_mp[1])
        if abs(move_x) < 50 and abs(move_y) < 50:
            return None
        overhead = 35
        move_x = move_x + overhead if move_x > 0 else move_x - overhead
        wind_mouse_move_camera(move_x, move_y)

    def update_targets(self, targets: list[tuple]) -> None:
        """Threading method: update targets property"""
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screen(self, screen: object) -> None:
        """Threading method: update screen property"""
        self.lock.acquire()
        self.screen = screen
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        sleep(self.INITIALIZING_SECONDS)
        while not self.stopped:
            if self.targets:
                self.follow_target(random.choice(self.targets))
            self.character_position = self.character.find(self.screen, threshold=0.8)
            sleep(self.main_loop_delay)

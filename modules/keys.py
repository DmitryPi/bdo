import logging
import pydirectinput
import random
import time

from pynput import keyboard, mouse
from threading import Thread


class KeyListener:
    def __init__(self):
        self.buff_keys = ['f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12']

    def on_press(self, key):
        pass

    def on_release(self, key):
        if key == keyboard.Key.end:
            logging.info(f'{__class__.__name__} stopped')
            return False
        elif key == keyboard.Key.insert:
            Thread(target=self.press_keys, args=(self.buff_keys,), daemon=True).start()

    def on_move(self, x, y):
        pass

    def on_click(self, x, y, button, pressed):
        pass

    def on_scroll(self, x, y, dx, dy):
        pass

    def press_keys(self, keys: list, delay=1.5):
        for key in keys:
            pydirectinput.press(key, interval=random.uniform(0.05, 0.12))
            time.sleep(delay)

    def run(self):
        logging.info(f'{__class__.__name__} started')
        with mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll) as listener:
            with keyboard.Listener(
                    on_press=self.on_press,
                    on_release=self.on_release) as listener:
                listener.join()

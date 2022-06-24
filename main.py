import cv2 as cv
import logging

from threading import Thread

from modules.bot import BlackDesertBot
from modules.camera import Camera
from modules.vision import Vision
from modules.keys import KeyListener
from modules.utils import load_config, grab_screen


if __name__ == '__main__':
    config = load_config()
    DEBUG = config.getboolean('MAIN', 'DEBUG')

    if config['MAIN']['DEBUG']:
        logging.basicConfig(
            level=logging.INFO,
            format='%(name)s - %(levelname)s - %(message)s')
        logging.info('DEBUG')
    else:
        pass

    vision = Vision('assets/vessel.png')
    bot = BlackDesertBot('guard')
    camera = Camera(Vision('assets/character.png'))
    key_listener = KeyListener(to_stop=[bot, camera])
    bot.start()
    camera.start()

    running = False
    while True:
        try:
            screen = grab_screen(window_name='Black Desert - 419022')
            targets = vision.find(screen, threshold=0.73, crop=[0, 0, 1920, 600])
            character_position = camera.character_position

            bot.update_screen(screen)
            bot.update_targets(targets)
            bot.update_character_position(character_position)

            camera.update_state(bot.state)
            camera.update_screen(screen)
            camera.update_targets(targets)

            bot.filter_ability_cooldowns()

            if DEBUG:
                result = targets + character_position
                screen = vision.draw_rectangles(cv.cvtColor(screen, cv.COLOR_BGR2RGB), result)
                screen = cv.resize(screen, (1200, 675))
                cv.imshow('Screen', screen)
                if cv.waitKey(1) == ord('q'):
                    bot.stop()
                    camera.stop()
                    cv.destroyAllWindows()
                    break
            else:
                if not running:
                    key_listener.start()
                    running = True
                if bot.stopped:
                    print('- Main loop stopped')
                    break
        except Exception as e:
            bot.stop()
            camera.stop()
            raise e

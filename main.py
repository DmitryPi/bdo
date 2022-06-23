import cv2 as cv
import logging
import sys

from modules.bot import BotState, BlackDesertBot
from modules.camera import Camera
from modules.vision import Vision
from modules.keys import KeyListener
from modules.utils import load_config, grab_screen


if __name__ == '__main__':
    config = load_config()
    DEBUG = config['MAIN']['DEBUG']

    if config['MAIN']['DEBUG']:
        logging.basicConfig(
            level=logging.INFO,
            format='%(name)s - %(levelname)s - %(message)s')
        logging.info('DEBUG')
    else:
        pass

    if 'bot' in sys.argv:
        vision = Vision('assets/kzarka.png')
        bot = BlackDesertBot('guard')
        camera = Camera(Vision('assets/character.png'))
        bot.start()
        camera.start()

        while True:
            try:
                screen = grab_screen(window_name='Black Desert - 419022')
                targets = vision.find(screen, threshold=0.65, crop=[425, 210, 1600, 940])
                character_position = camera.character_position
                result = targets + character_position

                bot.update_screen(screen)
                bot.update_targets(targets)
                bot.update_character_position(character_position)

                camera.update_state(bot.state)
                camera.update_screen(screen)
                camera.update_targets(targets)

                bot.filter_ability_cooldowns()

                if bot.state == BotState.INIT:
                    pass
                elif bot.state == BotState.SEARCHING:
                    pass
                elif bot.state == BotState.NAVIGATING:
                    pass
                elif bot.state == BotState.KILLING:
                    pass

                if DEBUG:
                    screen = vision.draw_rectangles(cv.cvtColor(screen, cv.COLOR_BGR2RGB), result)
                    screen = cv.resize(screen, (1200, 675))
                    cv.imshow('Screen', screen)
                    if cv.waitKey(1) == ord('q'):
                        bot.stop()
                        camera.stop()
                        cv.destroyAllWindows()
                        break
            except Exception as e:
                bot.stop()
                camera.stop()
                raise e
    else:
        key_listener = KeyListener()
        key_listener.run()

import cv2 as cv
import logging
import sys

from modules.bot import BotState, BlackDesertBot
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
        vision = Vision('assets/boar.png')
        bot = BlackDesertBot()
        bot.start()

        while True:
            screen = grab_screen(window_name='Black Desert - 418417')
            result = vision.find(screen, threshold=0.7, crop=[420, 175, 1600, 900])

            bot.update_screen(screen)
            bot.update_targets(result)
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
                    cv.destroyAllWindows()
                    break
    else:
        key_listener = KeyListener()
        key_listener.run()

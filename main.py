import cv2 as cv
import logging

from time import sleep

from modules.bot import BlackDesertBot, BotBuffer
from modules.camera import Camera
from modules.vision import Vision
from modules.keys import KeyListener
from modules.utils import load_config, grab_screen, send_telegram_msg


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

    vision = Vision()
    bot = BlackDesertBot()
    bot_buffer = BotBuffer(bot.buffs + bot.foods)
    camera = Camera()
    to_stop = [bot, bot_buffer, camera]
    key_listener = KeyListener(to_stop=to_stop)
    # bot.start()
    # bot_buffer.start()
    # camera.start()

    i = 0
    running = False
    while True:
        try:
            screen = grab_screen(region=[0, 0, 1920, 1080])
            buff_queue = bot_buffer.buff_queue
            targets = vision.find_ui(screen, 'camp_toofar')
            character_position = camera.character_position

            bot.update_screen(screen)

            sleep(1)
            bot.maid_chest_open()

            # bot.update_buff_queue(buff_queue)
            # bot.update_targets(targets)
            # bot.update_character_position(character_position)

            # bot_buffer.update_screen(screen)

            # camera.update_state(bot.state)
            # camera.update_screen(screen)
            # camera.update_targets(targets)

            # bot.filter_ability_cooldowns()

            # if not i % 100:  # send msg if armor durability low or weight limit
            #     if vision.find_ui(screen, 'durability'):
            #         send_telegram_msg('Durability low')
            #     if vision.find_ui(screen, 'weight_limit'):
            #         send_telegram_msg('Weight limit')

            if DEBUG:
                result = targets + character_position
                screen = vision.draw_rectangles(cv.cvtColor(screen, cv.COLOR_BGR2RGB), result)
                screen = cv.resize(screen, (1200, 675))
                cv.imshow('Screen', screen)
                if cv.waitKey(1) == ord('q'):
                    [thread.stop() for thread in to_stop]
                    cv.destroyAllWindows()
                    break
            else:
                if not running:
                    key_listener.start()
                    running = True
                if key_listener.pause:
                    print('- Pause')
                    sleep(1)
                if key_listener.stopped:
                    print('- Main loop stopped')
                    break
            i += 1
            sleep(bot.main_loop_delay)
        except Exception as e:
            [thread.stop() for thread in to_stop]
            raise e

import logging

from modules.keys import KeyListener
from modules.utils import load_config


if __name__ == '__main__':
    config = load_config()

    if config['MAIN']['DEBUG']:
        logging.basicConfig(
            level=logging.INFO,
            format='%(name)s - %(levelname)s - %(message)s')
        logging.info('DEBUG')
    else:
        pass

    key_listener = KeyListener()
    key_listener.run()

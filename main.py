import logging

from modules.db import Database
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

    db = Database()
    print(db)

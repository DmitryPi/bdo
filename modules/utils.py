import configparser
import codecs


def build_config(config_name='config.ini') -> None:
    config = configparser.ConfigParser()
    config['MAIN'] = {
        'debug': True,
    }
    config['BINANCE'] = {
        'api_key': '',
    }
    config['DB'] = {
        'table': 'bdo',
    }
    with open(config_name, 'w') as f:
        print('- Creating new config')
        config.write(f)


def load_config(config_fp='config.ini'):
    config = configparser.ConfigParser()
    try:
        config.read_file(codecs.open(config_fp, 'r', 'utf-8'))
    except FileNotFoundError:
        print('- Config not found')
        build_config()
        config.read_file(codecs.open(config_fp, 'r', 'utf-8'))
    return config


def handle_error(error, to_file=False, to_sentry=False):
    if to_file:
        with open('error_log.txt', 'a', encoding='utf-8') as f:
            f.write(error + '\n')
    elif to_sentry:
        pass
    else:
        raise error

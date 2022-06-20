import configparser
import codecs
import cv2
import numpy as np
import win32gui
import win32ui
import win32con
import win32api


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


def grab_screen(window_name=None, region=None):
    if window_name:
        hwin = win32gui.FindWindow(None, window_name)
        if not hwin:
            raise Exception('Window not found: {}'.format(window_name))
    else:
        hwin = win32gui.GetDesktopWindow()

    if window_name:
        left, top, width, height = win32gui.GetWindowRect(hwin)
        width = width - left
        height = height - left
    elif region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

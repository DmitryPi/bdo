import configparser
import codecs
import cv2
import numpy as np
import random
import win32gui
import win32ui
import win32con
import win32api

from datetime import datetime
from time import sleep
from telegram import Bot, ParseMode
from telegram.error import BadRequest

from .keys import Keys


keys = Keys()


def build_config(config_name='config.ini') -> None:
    config = configparser.ConfigParser()
    config['MAIN'] = {
        'debug': True,
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
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


def get_datetime_passed_seconds(time_stamp, time_now=None, reverse=False):
    date_fmt = '%Y-%m-%d %H:%M:%S'
    time_now = time_now if time_now else datetime.now()
    time_now = datetime.strptime(str(time_now).split('.')[0], date_fmt)
    time_stamp = datetime.strptime(str(time_stamp).split('.')[0], date_fmt)
    if reverse:
        time_passed = time_stamp - time_now
    else:
        time_passed = time_now - time_stamp
    return int(time_passed.total_seconds())


def wind_mouse(
        start_x, start_y, dest_x, dest_y,
        G_0=12, W_0=3, M_0=13, D_0=13, delay=False, move_mouse=lambda x, y: None):
    '''
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational force
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    '''
    sqrt3 = np.sqrt(3)
    sqrt5 = np.sqrt(5)
    current_x, current_y = start_x, start_y
    v_x = v_y = W_x = W_y = 0
    while (dist := np.hypot(dest_x - start_x, dest_y - start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
            W_y = W_y / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random() * 3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0 * (dest_x - start_x) / dist
        v_y += W_y + G_0 * (dest_y - start_y) / dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0 / 2 + np.random.random() * M_0 / 2
            v_x = (v_x / v_mag) * v_clip
            v_y = (v_y / v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))

        if move_x > 1900:  # fluid transition from 1920-0; 0-1920
            pos_x, pos_y = win32api.GetCursorPos()
            win32api.SetCursorPos((1920, pos_y))  # resets cursor at 0
            sleep(.1)
            break
        elif move_x < 20:
            pos_x, pos_y = win32api.GetCursorPos()
            win32api.SetCursorPos((0, pos_y))  # resets cursor at 1920
            sleep(.1)
            break

        if current_x != move_x or current_y != move_y:
            # This should wait for the mouse polling interval
            try:
                move_mouse(current_x := move_x, current_y := move_y)
            except TypeError:
                move_mouse((current_x := move_x, current_y := move_y))
            if delay:
                sleep(0.00001)
    return current_x, current_y


def wind_mouse_move_camera(x: int, y: int, step=13, delay=True, screen_size=(1920, 1080)) -> None:
    """Move from current position_x + x; current position_y + y
       Increase step to accelerate"""
    move_func = win32api.SetCursorPos
    pos_x, pos_y = win32api.GetCursorPos()
    screen_w, screen_h = screen_size
    x += pos_x
    y += pos_y
    wind_mouse(pos_x, pos_y, x, y, M_0=step, D_0=step, move_mouse=move_func, delay=delay)


def mouse_move_to(x: int, y: int, delay=0.2) -> None:
    pos_x, pos_y = win32api.GetCursorPos()
    wind_mouse(pos_x, pos_y, x, y, move_mouse=win32api.SetCursorPos)
    sleep(delay)


def show_cursor(key='i', rnd_range=[0.1, 0.25]):
    keys.directKey('i')
    sleep(random.uniform(*rnd_range))
    keys.directKey('i', keys.key_release)
    sleep(0.3)


def calc_rect_middle(rect: list[int]) -> list[int]:
    """Calculate middle point of rectangle"""
    x, y, w, h = rect
    x = int((x * 2 + w) / 2)
    y = int((y * 2 + h) / 2)
    return [x, y, w, h]


def send_telegram_msg(msg: str, photo_path='') -> None:
    try:
        chat_id = 5156307333
        bot = Bot('5563804245:AAHK0-VXb4D3FlBwQiFi9w6pJzio_ZqnbhU')
        if photo_path:
            bot.send_photo(chat_id, open(photo_path, 'rb'), caption=msg)
        else:
            bot.send_message(
                chat_id, msg,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                protect_content=True,
            )
    except BadRequest as e:
        print('- Error BadRequest:', e.message)
    except Exception as e:
        print('- Error Unknown:', repr(e))

import sys
import time
import pyautogui
import numpy as np
from math import sqrt

WEGO_X_LIST = [*range(382, 452),779,1018,1258,1378,1498,  *range(513, 568), 659, 899, 1138] #判斷x值範圍
WEGO_CHECKING_COLOR_A = '#262d39' #判斷威格上方顏色
WEGO_CHECKING_COLOR_B = '#99eeed' #判斷威格下方顏色
WEGO_CHECKING_Y_A = 544 #判斷威格上方位置Y值
WEGO_CHECKING_Y_B = 688 #判斷威格下方位置Y值
WEGO_XA_XB_distance = 786 - 779 #上方判斷點與下方判斷點X距離差距 (下減上)
WEGO_XA_COLOR_distance = 30 #色差範圍值
WEGO_XB_COLOR_distance = 5 #色差範圍值


SR_X_LIST = [664,904,1024,1144,1263,1383,1503, 425, 544, 784] #判斷x值範圍
SR_CHECKING_COLOR_A = '#f3f4f1' #判斷SR上方顏色
SR_CHECKING_COLOR_B = '#ac7bfe' #判斷SR下方顏色
SR_CHECKING_Y_A = 592 #判斷SR上方位置Y值
SR_CHECKING_Y_B = 691 #判斷SR下方位置Y值
SR_XA_XB_distance = 2 #上方判斷點與下方判斷點X距離差距 (下減上)
SR_XA_COLOR_distance = 5 #色差範圍值
SR_XB_COLOR_distance = 5 #色差範圍值


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def get_position_color(xy):
    try:
        screen = pyautogui.screenshot()
        r, g, b = screen.getpixel(xy)
        return rgb_to_hex(r, g, b)
    except Exception as e:
        return None

def get_position_color_s(xy, screen):
    try:
        r, g, b = screen.getpixel(xy)
        return rgb_to_hex(r, g, b)
    except Exception as e:
        return None

def wait_until_position_color(xy, hex):
    i = 0
    while i < 1000:
        if get_position_color(xy) == hex:
            return
        time.sleep(0.05)
        i += 1

def wego_in(x, screen):
    u = color_distance(get_position_color_s((x, WEGO_CHECKING_Y_A), screen), WEGO_CHECKING_COLOR_A)
    d = color_distance(get_position_color_s((x + WEGO_XA_XB_distance, WEGO_CHECKING_Y_B), screen), WEGO_CHECKING_COLOR_B)
    if d <= WEGO_XB_COLOR_distance  and u <= WEGO_XA_COLOR_distance:
        print('we', x, u, d)
        return True
    return False

def sr_in(x, screen):
    u = color_distance(get_position_color_s((x + SR_XA_XB_distance, SR_CHECKING_Y_B), screen), SR_CHECKING_COLOR_B)
    d = color_distance(get_position_color_s((x, SR_CHECKING_Y_A), screen), SR_CHECKING_COLOR_A)

    if u <= SR_XA_COLOR_distance and d <= SR_XB_COLOR_distance:
        print('sr', x, u, d)
        return True
    return False

def is_wego_in():
    screen = pyautogui.screenshot()
    li = WEGO_X_LIST
    for i in li:
        if wego_in(i, screen):
            return True
    return False

def is_sr_in():
    screen = pyautogui.screenshot()

    li = SR_X_LIST
    for i in li:
        if sr_in(i, screen):
            return True
    return False

def color_distance(ha, hb):
    r, g, b = hex_to_rgb(ha)
    cr, cg, cb = hex_to_rgb(hb)
    color_diff = sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
    return color_diff


def get_color():
    mouse_now = None
    while True:

        if mouse_now != pyautogui.position():
            mouse_now = pyautogui.position()
            color_hex = get_position_color(mouse_now)

            print(mouse_now, color_hex)
        time.sleep(0.05)


if __name__ == '__main__':
    i = 0
    mouse_now = None
    while i < 500:
        # 判斷再抽一次按鈕是否出現
        wait_until_position_color((1274, 889), '#59c9ff')

        # 判斷sr劍及UR炸彈是否出現
        if is_sr_in() and is_wego_in():
            print('found')
            break

        pyautogui.click(1274, 889)
        time.sleep(0.1)

        # 判斷確認按鈕是否出現
        wait_until_position_color((1055, 641), '#404040')
        time.sleep(0.5)
        pyautogui.click(1055, 641)
        time.sleep(0.1)

        # 判斷skip按鈕是否出現
        wait_until_position_color((1598, 152), '#ffffff')
        pyautogui.click(1592, 154)
        time.sleep(0.1)

        i += 1




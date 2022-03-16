import board, digitalio
import time

# import my modules here
from menu import Menu
from encoder import Encoder
from screen import Screen
from scale import Scale
from page import Page

import parameter as PARAS

# setup board led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# initialize load cell
scale = Scale(board.GP14, board.GP15)

# initialize ec11 encoder
ec11_encoder = Encoder(board.GP4, board.GP3, board.GP2)

# initialize lcd screen
screen = Screen(board.GP1, board.GP0)

# initialize a Setting instance
rom = PARAS.Setting()



def update_style1(name):
    return rom.get(name)

def update_style2(name1, name2):
    return (rom.get(name1), rom.get(name2))

def display_style1(name, value):
    return "{}: {}".format(name, value)

def display_style2(name, showing_value, value):
    return "{}: {}/{}".format(name, showing_value, value)

# weight display in Main Page
weight_display = Menu("WEIGHT", 2, 0)

def weight_update_style(name):
    return (scale.get_weight(), rom.get(name))

weight_display.update_func = weight_update_style(PARAS.MAX_WEIGHT)
weight_display.content_func = display_style2(PARAS.MAX_WEIGHT)
# counter display in Main Page
counter_display = Menu('COUNTER', 3, 0)
counter_display.update_func = update_style2(PARAS.CURRENT_CNT, PARAS.MAX_CNT)
counter_display.content_func = display_style2(PARAS.CURRENT_CNT, PARAS.MAX_CNT)


# initialize menu to be dispalyed on the lcd screen
value_menu = Menu("Value", 0, 0)
offset_menu = Menu("OFFSET", 1, 0)
factor_menu = Menu("FACTOR", 2, 0)

# setting up the pages
main_page = Page('Main', [weight_display, counter_display])
calibration_page= Page("Calibration", [value_menu, offset_menu, factor_menu, weight_menu])

while True:
    if ec11_encoder.button_pressed():
        screen.clear()
        screen.home()
        screen.print("Please wait...")
        scale.tare()
        screen.print("Done")
        ec11_encoder.btn_state = False

    # value_menu.update(scale.get_reading())
    # offset_menu.update(scale.get_offset())
    # factor_menu.update(scale.get_factor())
    # weight_menu.update(scale.get_weight())

    main_page.display(screen)
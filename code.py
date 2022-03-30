import board, digitalio
import time

# import my modules here
from encoder import Encoder
from screen import Screen
from scale import Scale
from item import Item
from controller import Controller

import parameter as PARAS

# setup board led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# initialize a Setting instance
rom = PARAS.Setting()
rom.print_settings()

# initialize load cell
scale = Scale(board.GP14, board.GP15, rom)

# initialize ec11 encoder
ec11_encoder = Encoder(board.GP4, board.GP3, board.GP2)

# initialize lcd screen
screen = Screen(board.GP1, board.GP0)

# Main Page, Row 0, displaying current_weight/max_weight
unit_weight_item = Item("READ_WEIGHT", x=0, y=8, need_refresh=True)
unit_weight_item.update_func = lambda: "{:>6}".format(scale.get_weight())

max_weight_item = Item(PARAS.MAX_WEIGHT)
max_weight_item.update_func = lambda: "{:.1f}".format(rom.get(PARAS.MAX_WEIGHT))

# Main Page, Row 1, displaying current_cnt/max_cnt
current_cnt_item = Item(PARAS.CURRENT_CNT)
current_cnt_item.update_func = lambda: "{:05d}".format(rom.get(PARAS.CURRENT_CNT))

max_cnt_item = Item(PARAS.MAX_CNT)
max_cnt_item.update_func = lambda: "{}".format(rom.get(PARAS.MAX_CNT))

# Main Page, Row 3, single menu jump to Setting Page
setting_link = Item("PRESS TO SETTINGS", x=3, y=0)

# Main Page
entry_page = [
    ["WEIGHT: ", unit_weight_item, "/", max_weight_item],
    ["COUNTER: ", current_cnt_item, "/", max_cnt_item],
    [],
    [setting_link]
]

# Calibrate Page, Row 0, displaying raw value read from hx711 sensor
raw_value_item = Item("Value", x=0, y=0, need_refresh=True)
raw_value_item.update_func = lambda: scale.get_value()

# Calibrate Page, Row 1, displaying offset
offset_item = Item("OFFSET", x=1, y=0, need_refresh=True)
offset_item.update_func = lambda: scale.get_offset()

# Calibrate Page, Row 2, displaying factor
factor_item = Item("FACTOR", x=2, y=0, need_refresh=True)
factor_item.update_func = lambda: scale.get_factor()

# Calibrate Page, Row 3, displaying current weight
calibrate_save_link = Item("SAVE AND EXIT", x=3, y=0)

calibrate_page = [
    ["RAW VALUE:", raw_value_item],
    ["OFFSET:", offset_item],
    ["FACTOR:", factor_item],
    [calibrate_save_link]
]

# Config Page
weight_link = Item("MAX WEIGHT", x=0, y=0, need_cursor=True)
counter_link = Item("MAX COUNTER", x=1, y=0, need_cursor=True)
calibrate_link = Item("CALIBRATE SCALE", x=2, y=0, need_cursor=True)
return_link = Item("RETURN", x=3, y=0, need_cursor=True)
# Config Page
setting_page = [
    ["1. ", weight_link],
    ["2. ", counter_link],
    ["3. ", calibrate_link],
    ["4. ", return_link]
]

#connecting pages via the elements
setting_link.link = setting_page
calibrate_link.link = calibrate_page

weight_link.link = entry_page
counter_link.link = entry_page
return_link.link = entry_page

calibrate_save_link.link = entry_page

# initial setup for the controller
controller = Controller(entry_page)
screen.show(entry_page)

while True:
    # handle encoder button press event
    if ec11_encoder.button_pressed():
        # update current page in order to show correct
        controller.change_page()
        screen.clear()
        screen.show(controller.page)
        # reset button state
        ec11_encoder.btn_state = False

    ec11_encoder.posistion_changed()

    if ec11_encoder.increase_state:
        controller.move_next_link()
        # reset encoder increase state
        ec11_encoder.increase_state = False

    if ec11_encoder.decrease_state:
        controller.move_prev_link() 
        # reset encoder decrease state
        ec11_encoder.decrease_state = False

    # update current item in order to show correct blinking cursor
    screen.partial_show(controller.refresh_items)
    if controller.link.need_cursor:
        print(f"link name: {controller.link.name}")
        screen.cursor_blink(controller.link.x, controller.link.y)
    else:
        screen.cursor_hide()
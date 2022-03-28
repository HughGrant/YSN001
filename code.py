import board, digitalio
import time

# import my modules here
from encoder import Encoder
from screen import Screen
from scale import Scale
from page import Page, Item

import parameter as PARAS

# setup board led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# initialize a Setting instance
rom = PARAS.Setting()

# initialize load cell
scale = Scale(board.GP14, board.GP15, rom)

# initialize ec11 encoder
ec11_encoder = Encoder(board.GP4, board.GP3, board.GP2)

# initialize lcd screen
screen = Screen(board.GP1, board.GP0)



# Main Page, Row 0, displaying current_weight/max_weight
unit_weight_item = Item("READ_WEIGHT", always_refresh=True)
unit_weight_item.update_func = lambda: "{:>6}".format(scale.get_weight())

max_weight_item = Item(PARAS.MAX_WEIGHT)
max_weight_item.update_func = lambda: "{:.1f}".format(rom.get(PARAS.MAX_WEIGHT))

# Main Page, Row 1, displaying current_cnt/max_cnt
current_cnt_item = Item(PARAS.CURRENT_CNT)
current_cnt_item.update_func = lambda: "{:05d}".format(rom.get(PARAS.CURRENT_CNT))

max_cnt_item = Item(PARAS.MAX_CNT)
max_cnt_item.update_func = lambda: "{}".format(rom.get(PARAS.MAX_CNT))

# Main Page, Row 2, single menu jump to Setting Page
setting_link = Item("SETTING", linkable=True)

# Main Page, Row 3, single menu jump to Calibrate Page
calibrate_link = Item("CALIBRATE SCALE", linkable=True)

# assemble Main Page
main_page = Page("MAIN", [
    ["WEIGHT: ", unit_weight_item, "/", max_weight_item],
    ["COUNTER: ", current_cnt_item, "/", max_cnt_item],
    setting_link,
    calibrate_link,
])

# Calibrate Page, Row 0, displaying raw value read from hx711 sensor
raw_value_item = Item("Value")
raw_value_item.update_func = lambda: scale.get_value()

# Calibrate Page, Row 1, displaying offset
offset_item = Item("OFFSET")
offset_item.update_func = lambda: scale.get_offset()

# Calibrate Page, Row 2, displaying factor
factor_item = Item("FACTOR")
factor_item.update_func = lambda: scale.get_factor()

# Calibrate Page, Row 3, displaying current weight
# unit_weight_item

calibrate_page = Page("CALIBRATION", [
    ["RAW VALUE: ", raw_value_item],
    ["OFFSET:", offset_item],
    ["FACTOR:", factor_item],
    ["WEIGHT:", unit_weight_item]
])
calibrate_link.page = calibrate_page

# Config Page

config_page = Page("CONFIG", [
    ["MAX WEIGHT: ", max_weight_item],
    ["MAX_COUNTER: ", max_cnt_item],
    "PLACE HOLDER 1",
    "PLACE HOLDER 2"
])
setting_link.page = config_page

#connecting pages via the elements

# initial cursor position element
current_page = None

while True:
    # if ec11_encoder.rotary_increase():
    #     pass

    # if ec11_encoder.rotary_decrease():
    #     pass

    # if ec11_encoder.button_pressed():
    #     screen.clear()
    #     screen.home()
    #     screen.print("Please wait...")
    #     scale.tare()
    #     screen.print("Done")
    #     ec11_encoder.btn_state = False
    if current_page is None:
        current_page = main_page
        screen.display(main_page)
    else:
        screen.display(current_page)

    screen.cursor_blink()
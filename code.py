import board, digitalio
import time

# import my modules here
from encoder import Encoder
from screen import Screen
from scale import Scale
from page import Page, Row, Element

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

# weight display in Main Page
raw_weight = Element("READ_WEIGHT", True)
raw_weight.update_func = lambda: scale.get_weight()
max_weight = Element(PARAS.MAX_WEIGHT)
max_weight.update_func = lambda: rom.get(PARAS.MAX_WEIGHT)
weight_row = Row("WEIGHT", [raw_weight, max_weight], True)
weight_row.display_func = lambda values: "WEIGHT: {:>4}/{}".format(*values)

# counter display in Main Page
current_cnt = Element(PARAS.CURRENT_CNT)
current_cnt.update_func = lambda: rom.get(PARAS.CURRENT_CNT) 
max_cnt = Element(PARAS.MAX_CNT)
max_cnt.update_func = lambda: rom.get(PARAS.MAX_CNT)
counter_row = Row("COUNTER", [current_cnt, max_cnt])
counter_row.display_func = lambda values: "COUNTER: {:05d}/{}".format(*values)

# initialize menu to be dispalyed on the lcd screen
value_menu = Element("Value")
offset_menu = Element("OFFSET")
factor_menu = Element("FACTOR")

# setting up the pages
main_page = Page('Main', [weight_row, counter_row])
calibration_page= Page("Calibration", [value_menu, offset_menu, factor_menu])

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
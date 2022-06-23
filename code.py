import board, digitalio, analogio
import time

from lib.adafruit_debouncer import Debouncer

# import my modules here
from encoder import Encoder
from screen import Screen
from scale import Scale
from link import Link
from controller import Controller
from x9c import X9C

import parameter as PS

# setup buttons
start_btn_pin = digitalio.DigitalInOut(board.GP16)
start_btn_pin.direction = digitalio.Direction.INPUT
start_btn_pin.pull = digitalio.Pull.UP
start_btn = Debouncer(start_btn_pin)

# setup board led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# initialize a Setting instance
rom = PS.Setting()
rom.print_settings()

# initialize load cell
pin_data = board.D5
pin_clk = board.D6
scale = Scale(board.GP14, board.GP15, rom)

# initialize ec11 encoder
ec11 = Encoder(board.GP4, board.GP3, board.GP2)

# initialize lcd screen
screen = Screen(board.GP1, board.GP0)


# define a fine for lambda usage
def goto(page):
    controller.crt_page = page
    controller.gather_links()
    screen.lcd.clear()
    screen.display(page)


# shared return link
shared_return_link = Link("RETURN TO MAIN")
# TODO: whenever returned back to main page, we should update the corresponding text
shared_return_link.press_func = lambda: goto(entry_page)

# Main Page, Row 1, displaying current_weight/max_weight
unit_weight_item = Link("READ_WEIGHT")
unit_weight_item.update_func = lambda: "{:>6}".format(scale.get_weight())

max_weight_item = Link(PS.MAX_WEIGHT)
max_weight_item.update_func = lambda: "{:.1f}".format(rom.get(PS.MAX_WEIGHT))

# Main Page, Row 2, displaying current_cnt/max_cnt
current_cnt_item = Link(PS.CURRENT_CNT)
current_cnt_item.update_func = lambda: "{:05d}".format(rom.get(PS.CURRENT_CNT))

max_cnt_item = Link(PS.MAX_CNT)
max_cnt_item.update_func = lambda: "{}".format(rom.get(PS.MAX_CNT))

# Main Page, Row 3, progress bar
filling_process_bar = ["-" * screen.max_cols]
# Main Page, Row 4, single menu jump to Setting Page
enter_config_link = Link("PRESS KNOB TO CONFIG")
enter_config_link.press_func = lambda: goto(config_page)

entry_page = [
    ["WEIGHT: ", str(unit_weight_item), "/",
     str(max_weight_item)],
    ["COUNTER: ", str(current_cnt_item), "/",
     str(max_cnt_item)],
    filling_process_bar,
    [enter_config_link],
]

# Calibrate Page, Row 0, displaying raw value read from hx711 sensor
raw_value_item = Link("Value")
raw_value_item.update_func = lambda: scale.get_value()

# Calibrate Page, Row 1, displaying offset
offset_item = Link("OFFSET")
offset_item.update_func = lambda: scale.get_offset()

# Calibrate Page, Row 2, displaying factor
factor_item = Link("SCALAR")
factor_item.update_func = lambda: scale.get_factor()

# Calibrate Page, Row 3, displaying current weight
calibrate_save_link = Link("SAVE AND EXIT")

calibration_page = [
    ["RAW VALUE:", raw_value_item],
    ["OFFSET:", offset_item],
    ["SCALAR:", factor_item],
    [calibrate_save_link],
]

tare_item = Link("TARE")
tare_item.press_func = lambda: print("taring done!!!")

calibration_item = Link("CALIBRATION")

scale_page = [
    ["1. ", tare_item],
    ["2. ", calibration_item],
    [],
    ["   ", shared_return_link],
]

# Config Page
weight_link = Link("MAX WEIGHT")
counter_link = Link("MAX COUNTER")
scale_link = Link("SCALE SETTINGS")
# Config Page
config_page = [
    ["1. ", weight_link],
    ["2. ", counter_link],
    ["3. ", scale_link],
    ["   ", shared_return_link],
]

# Counter Page
cnt_crt_value = rom.get(PS.MAX_CNT)
cnt_config_item = Link(cnt_crt_value)
cnt_config_item.config_val = cnt_crt_value
cnt_config_item.max_display_val = rom.get(PS.MAX_DISPLAY_CNT)
cnt_config_item.min_display_val = 1


def generate_num_link(num: int) -> Link:
    num_link = Link("NUM_PADS_" + str(num))
    num_link.config_val = num
    num_link.press_func = lambda: num
    return num_link


# reusable number pads
num_pads = [generate_num_link(x) for x in range(10)]
num_pads_with_seperator = []
for num in num_pads:
    num_pads_with_seperator.append(num)
    num_pads_with_seperator.append("|")

cnt_save_link = Link("SAVE")
cnt_reset_link = Link("RESET")
cnt_save_link.press_func = lambda: print("saved")
cnt_reset_link.press_func = lambda: print("reset")

counter_config_page = [
    [cnt_config_item],
    [
        "RANGE: ", cnt_config_item.min_display_val, "-",
        cnt_config_item.max_display_val
    ],
    num_pads_with_seperator,
    [cnt_reset_link, " ", cnt_save_link],
]

weight_link.page = entry_page

calibrate_save_link.page = entry_page
cnt_config_item.page = entry_page

# avoid to display the whole page in the while loop
# it will slow the program very much
controller = Controller(entry_page)

screen.display(controller.crt_page)

scale_link.press_func = lambda: goto(scale_page)
counter_link.press_func = lambda: goto(counter_config_page)

# setup digital pot x9c
a0 = analogio.AnalogIn(board.A0)
x9c = X9C(cs=board.GP22, inc=board.GP21, ud=board.GP20)

WORKING_MODE = False
CONFIG_MODE = True

while CONFIG_MODE:
    # constantly update states here
    start_btn.update()
    ec11.update()

    if start_btn.fell:
        print("just pressed start btn")

    if ec11.btn.fell:
        controller.knob_press()

    if ec11.increase:
        controller.move_next_link()

    if ec11.decrease:
        controller.move_prev_link()

    # show correct blinking cursor
    if len(controller.links) > 1:
        screen.cursor_pos(controller.crt_link.x, controller.crt_link.y)
        time.sleep(0.001)
    else:
        screen.cursor_hide()

    # TODO: should we update the read weight here constantly

while WORKING_MODE:
    print("working mode now")

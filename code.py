import board, digitalio, analogio
import time

# import my modules here
from encoder import Encoder
from screen import Screen
from scale import Scale
from link import Link
from controller import Controller
from x9c import X9C

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

# shared return link
shared_return_link = Link("RETURN TO MAIN", type="FUNC")

# Main Page, Row 0, displaying current_weight/max_weight
unit_weight_item = Link("READ_WEIGHT", need_refresh=True)
unit_weight_item.update_func = lambda: "{:>6}".format(scale.get_weight())

max_weight_item = Link(PARAS.MAX_WEIGHT)
max_weight_item.update_func = lambda: "{:.1f}".format(rom.get(PARAS.MAX_WEIGHT))

# Main Page, Row 1, displaying current_cnt/max_cnt
current_cnt_item = Link(PARAS.CURRENT_CNT)
current_cnt_item.update_func = lambda: "{:05d}".format(rom.get(PARAS.CURRENT_CNT))

max_cnt_item = Link(PARAS.MAX_CNT)
max_cnt_item.update_func = lambda: "{}".format(rom.get(PARAS.MAX_CNT))

# Main Page, Row 3, single menu jump to Setting Page
enter_config_link = Link("PRESS KNOB TO CONFIG", type="FUNC")

# Main Page
entry_page = [
    ["WEIGHT: ", unit_weight_item, "/", max_weight_item],
    ["COUNTER: ", current_cnt_item, "/", max_cnt_item],
    ["-" * screen.max_cols],
    [enter_config_link],
]

# Calibrate Page, Row 0, displaying raw value read from hx711 sensor
raw_value_item = Link("Value")
raw_value_item.update_func = lambda: scale.get_value()

# Calibrate Page, Row 1, displaying offset
offset_item = Link("OFFSET")
offset_item.update_func = lambda: scale.get_offset()

# Calibrate Page, Row 2, displaying factor
factor_item = Link("FACTOR")
factor_item.update_func = lambda: scale.get_factor()

# Calibrate Page, Row 3, displaying current weight
calibrate_save_link = Link("SAVE AND EXIT")

calibration_page = [
    ["RAW VALUE:", raw_value_item],
    ["OFFSET:", offset_item],
    ["FACTOR:", factor_item],
    [calibrate_save_link],
]

tare_item = Link("TARE", type="FUNC")
tare_item.press_func = lambda: print("taring done!!!")

calibration_item = Link("CALIBRATION", type="FUNC")

scale_page = [
    ["1. ", tare_item],
    ["2. ", calibration_item],
    [],
    ["   ", shared_return_link],
]

# Config Page
weight_link = Link("MAX WEIGHT", type="FUNC")
counter_link = Link("MAX COUNTER", type="FUNC")
scale_link = Link("SCALE SETTINGS", type="FUNC")
# Config Page
config_page = [
    ["1. ", weight_link],
    ["2. ", counter_link],
    ["3. ", scale_link],
    ["   ", shared_return_link],
]

# Counter Page
cnt_config_item = Link("CNT_CONFIG", type="CONF")
cnt_config_item.config_val = rom.get(PARAS.MAX_CNT)
cnt_config_item.max_display_val = rom.get(PARAS.MAX_DISPLAY_CNT)
cnt_config_item.min_display_val = 1

cnt_save_link = Link("SAVE", type="FUNC")
cnt_reset_link = Link("RESET", type="FUNC")
counter_config_page = [
    [cnt_config_item],
    ["RANGE: ", cnt_config_item.min_display_val, "-", cnt_config_item.max_display_val],
    ["1|2|3|4|5|6|7|8|9|0"],
    [cnt_reset_link, " ", cnt_save_link],
]

weight_link.page = entry_page

calibrate_save_link.page = entry_page
cnt_config_item.page = entry_page

# initial setup for the controller
controller = Controller(entry_page)
screen.show(entry_page)


def goto(page):
    controller.crt_page = page
    controller.gather_links()


enter_config_link.press_func = lambda: goto(config_page)
scale_link.press_func = lambda: goto(scale_page)
counter_link.press_func = lambda: goto(counter_config_page)
shared_return_link.press_func = lambda: goto(entry_page)


cnt_save_link.press_func = lambda: print("saved")
cnt_reset_link.press_func = lambda: print("reset")

# setup digital pot x9c
a0 = analogio.AnalogIn(board.A0)
x9c = X9C(cs=board.GP22, inc=board.GP21, ud=board.GP20)

while True:
    print(
        "value: ",
        a0.value,
        " voltage: ",
        (a0.value * a0.reference_voltage) / 65536,
        " step: ",
        x9c.crt_step,
    )
    # print("voltage:", (a0.value * 3.3) / 65536)
    time.sleep(0.1)
    # handle encoder button press event
    if ec11_encoder.button_pressed():
        # update current page in order to show correct
        controller.knob_press()
        if len(controller.refresh_items) >= 1:
            screen.cursor_hide()
        screen.lcd.clear()
        screen.show(controller.crt_page)
        # reset button state
        ec11_encoder.btn_state = False

    ec11_encoder.posistion_changed()

    if ec11_encoder.increase_state:
        x9c.trim_pot(66, True)
        controller.knob_increase()
        # reset encoder increase state
        ec11_encoder.increase_state = False

    if ec11_encoder.decrease_state:
        x9c.trim_pot(0, True)
        controller.knob_decrease()
        # reset encoder decrease state
        ec11_encoder.decrease_state = False

    # show correct blinking cursor
    screen.partial_show(controller.refresh_items)
    if len(controller.refresh_items) == 0:
        screen.cursor_blink(controller.crt_item.x, controller.crt_item.y)

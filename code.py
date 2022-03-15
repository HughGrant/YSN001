import board, digitalio

# import my modules here
from menu import Menu
from encoder import Encoder
from screen import Screen
from scale import Scale
from page import Page

# setup board led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# initialize load cell
scale = Scale(board.GP15, board.GP14)

# initialize ec11 encoder
ec11_encoder = Encoder(board.GP4, board.GP3, board.GP2)

# initialize lcd screen
screen = Screen(board.GP1, board.GP0)

# initialize menu to be dispalyed on the lcd screen

value_menu = Menu("Value", 0, 0)
offset_menu = Menu("OFFSET", 1, 0)
factor_menu = Menu("FACTOR", 2, 0)
weight_menu = Menu("WEIGHT", 3, 0)

main_screen = Page("Main Screen", [value_menu, offset_menu, factor_menu, weight_menu])

while True:
    scale.get_value()
    # main_screen.display(screen)

    # if ec11_encoder.button_pressed():
    #     screen.clear()
    #     scale.tare()

    # value_menu.update(scale.get_reading())
    # offset_menu.update(scale.get_offset())
    # factor_menu.update(scale.get_factor())
    # weight_menu.update(scale.get_weight())
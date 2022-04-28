from lib.lcd.lcd import LCD
from lib.lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lib.lcd.lcd import CursorMode

import busio, microcontroller

from link import Link


class Screen:
    def __init__(
        self,
        scl: microcontroller.Pin,
        sda: microcontroller.Pin,
        cols: int = 20,
        rows: int = 4,
        address: str = 0x27,
    ) -> None:
        self.max_cols = cols
        self.max_rows = rows
        # setup i2c for lcd display
        i2c = busio.I2C(scl, sda)
        self.lcd = LCD(I2CPCF8574Interface(i2c, address), cols, rows)

    def display(self, links: list[list]) -> None:
        for i, row in enumerate(links):
            self.lcd.set_cursor_pos(i, 0)
            for t in row:
                self.lcd.print(str(t))

    def cursor_pos(self, row: int = 0, col: int = 0) -> None:
        self.lcd.set_cursor_pos(row, col)
        self.lcd.set_cursor_mode(CursorMode.BLINK)

    def cursor_hide(self) -> None:
        self.lcd.set_cursor_mode(CursorMode.HIDE)

    # probably should get rid of this
    # def get_i2c_address(self) -> str:
    #     while not self.i2c.try_lock():
    #         print("i2c tring to get the lock, please wait")

    #     try:
    #         address = self.i2c.scan()[0]
    #         print("i2c address for lcd:", hex(address))
    #     finally:
    #         self.i2c.unlock()
    #     return hex(address)

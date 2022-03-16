from lib.lcd.lcd import LCD
from lib.lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lib.lcd.lcd import CursorMode

import busio, board, microcontroller

try:
    from typing import Any
except ImportError:
    pass

class Screen:
    def __init__(
        self,
        scl: microcontroller.Pin,
        sda: microcontroller.Pin,
        col: int = 24,
        rows: int = 4,
        address: str = 0x27
    ) -> None:
        # setup i2c for lcd display
        i2c = busio.I2C(scl, sda)
        self.lcd = LCD(I2CPCF8574Interface(i2c, address))
    
    def set_cursor_pos(self, row: int, col: int) -> None:
        self.lcd.set_cursor_pos(row, col)
    
    def print(self, content: Any) -> None:
        self.lcd.print(content)
    
    def clear(self) -> None:
        self.lcd.clear()
    
    def home(self) -> None:
        self.lcd.home()
    
    def get_i2c_address(self) -> str:
        while not self.i2c.try_lock():
            print("i2c tring to get the lock, please wait")

        try:
            address = self.i2c.scan()[0]
            print("i2c address for lcd:", hex(address))
        finally:
            self.i2c.unlock()
        return hex(address)
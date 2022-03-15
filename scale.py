from lib.hx711.hx711_gpio import HX711
import board, digitalio, microcontroller

import parameter as rom

class Scale:
    def __init__(
        self, 
        slk: microcontroller.Pin,
        dat: microcontroller.Pin
    ) -> None:
        # setup for hx711
        self.slk = digitalio.DigitalInOut(slk)
        self.dat = digitalio.DigitalInOut(dat)
        self.slk.direction = digitalio.Direction.OUTPUT
        # init scale
        self.hx = HX711(self.slk, self.dat)
    
        self.hx.set_offset(rom.get('OFFSET'))
        self.hx.set_scale(rom.get('FACTOR'))

    def get_weight(self) -> float:
        return self.hx.get_round_units()
    
    def get_reading(self) -> int:
        return self.hx.read()

    def get_value(self) -> float:
        return self.hx.get_value()
    
    def get_offset(self) -> float:
        return self.hx.OFFSET

    def get_factor(self) -> float:
        return self.hx.FACTOR

    def tare(self):
        self.hx.tare()
        rom.write('OFFSET', self.hx.OFFSET)
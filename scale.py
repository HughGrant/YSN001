import board, digitalio, microcontroller

from lib.hx711.hx711_pio import HX711_PIO
from parameter import Setting


class Scale:

    def __init__(self, pin_data: microcontroller.Pin,
                 pin_clk: microcontroller.Pin, rom: Setting) -> None:
        # setup for hx711
        self.hx = HX711_PIO(self.pin_data, self.pin_clk, tare=True)
        self.rom = rom
        # set scale data read from flash
        self.hx.offset = self.rom.get('OFFSET')
        self.hx.set_scale = self.rom.get('SCALAR')

    def debug(self) -> None:
        reading = self.hx.read(5)
        reading_raw = self.hx.read_raw()
        print("[{: 8.2f} g] [{: 8} raw] offset: {}, scalar: {}".format(
            reading, reading_raw, self.hx.offset, self.hx.scalar))

    def get_weight(self) -> float:
        return self.hx.get_round_units()

    def get_value(self) -> float:
        return self.hx.get_value()

    def tare(self, placed_weight: float):
        scalar = self.hx.determine_scalar(placed_weight)
        self.rom.save('SCALAR', scalar)
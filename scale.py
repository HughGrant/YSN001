import board, digitalio, microcontroller

from lib.hx711.hx711_gpio import HX711_GPIO
import parameter


class Scale:

    def __init__(self, data: microcontroller.Pin, clk: microcontroller.Pin,
                 rom: parameter.Setting) -> None:

        self.hx = HX711_GPIO(pin_data=digitalio.DigitalInOut(data),
                             pin_clk=digitalio.DigitalInOut(clk),
                             tare=True)
        self.rom = rom
        # set scale data read from flash
        self.hx.offset = self.rom.get('OFFSET')
        self.hx.scalar = self.rom.get('SCALAR')

    def debug(self) -> None:
        reading = self.hx.read(5)
        reading_raw = self.hx.read_raw()
        print("[{: 8.2f} g] [{: 8} raw] offset: {}, scalar: {}".format(
            reading, reading_raw, self.hx.offset, self.hx.scalar))

    def tare(self) -> None:
        self.hx.tare()
        self.rom.save(parameter.OFFSET, self.hx.offset)
        self.rom.write()

    def read(self, average_count: int = 1) -> float:
        return self.hx.read(average_count)

    def read_raw(self) -> int:
        return self.hx.read_raw()

    def read_average(self, count: int = 10) -> int:
        return self.hx.read_average(count)

    def determine_scalar(self, placed_weight: float):
        scalar = self.hx.determine_scalar(placed_weight)
        self.rom.save(parameter.SCALAR, scalar)
        self.rom.write()
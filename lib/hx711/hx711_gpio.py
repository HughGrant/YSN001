import board
import time

class HX711:
    def __init__(self, pd_sck, dout, gain: int=128) -> None:
        self.pSCK = pd_sck
        self.pOUT = dout
        self.pSCK.value = False

        self.GAIN: int = 0
        self.OFFSET: float = 0.0
        self.SCALE: float = 1.0
        self.last_val: int = 0.0

        self.set_gain(gain)

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        self.read()

    def is_ready(self) -> bool:
        return self.pOUT == 0

    def read(self) -> int:
        # wait for the device being ready
        for _ in range(500):
            if self.pOUT.value == 0:
                break
            time.sleep(0.0125)
        else:
            raise OSError("Sensor does not respond")

        # shift in data, and gain & channel info
        result = 0
        for j in range(24 + self.GAIN):
          #  state = disable_irq()
            self.pSCK.value = True
            self.pSCK.value = False
          #  enable_irq(state)
            result = (result << 1) | self.pOUT.value

        # shift back the extra bits
        result >>= self.GAIN

        # check sign
        if result > 0x7fffff:
            result -= 0x1000000

        self.last_val = result
        return result

    def read_average(self, times: int=3) -> float:
        sum = 0
        for _ in range(times):
            sum += self.read()
        return sum / times


    def get_value(self) -> int:
        return self.read() - self.OFFSET
    
    def get_units(self) -> float:
        return self.get_value() / self.SCALE

    def get_round_units(self) -> float:
        weight =self.get_units()
        print("weight: ", weight)
        if weight < 0.0:
            weight = 0.0

        weight = round(weight, 1)
        return weight

    def tare(self, times=15) -> None:
        self.set_offset(self.read_average(times))

    def set_scale(self, scale) -> None:
        self.SCALE = scale

    def set_offset(self, offset) -> None:
        self.OFFSET = offset

    def power_down(self):
        self.pSCK.value(False)
        self.pSCK.value(True)

    def power_up(self):
        self.pSCK.value(False)
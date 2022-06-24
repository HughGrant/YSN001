import digitalio, rotaryio, board
from link import Link
from lib.adafruit_debouncer import Debouncer


class Encoder:

    def __init__(self, channelA, channelB, button) -> None:
        # setup ec11 rotary encoder
        # switch channel A&B will change the direction
        self.rotary = rotaryio.IncrementalEncoder(channelA, channelB)
        # setup debounce button
        btn_pin = digitalio.DigitalInOut(button)
        btn_pin.direction = digitalio.Direction.INPUT
        btn_pin.pull = digitalio.Pull.UP
        self.btn = Debouncer(btn_pin)
        # initialize encoder position
        self.increase = False
        self.decrease = False
        self.last_pos = self.rotary.position
        self.counter = 0

    def update(self) -> int:
        # update status
        self.increase = False
        self.decrease = False
        self.btn.update()
        # compare position int value
        current_pos = self.rotary.position
        pos_change = current_pos - self.last_pos
        if pos_change > 0:
            self.increase = True
        if pos_change < 0:
            self.decrease = True
        # save current position value
        self.last_pos = current_pos

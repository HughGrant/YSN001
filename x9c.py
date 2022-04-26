import digitalio, time
from microcontroller import Pin


class X9C:
    def __init__(self, cs: Pin = None, inc: Pin = None, ud: Pin = None) -> None:
        self._cs = digitalio.DigitalInOut(cs)  # chip select
        self._inc = digitalio.DigitalInOut(inc)  # increase
        self._ud = digitalio.DigitalInOut(ud)  # up or down

        self._cs.direction = digitalio.Direction.OUTPUT
        self._inc.direction = digitalio.Direction.OUTPUT
        self._ud.direction = digitalio.Direction.OUTPUT

        self.max_step = 99
        self.min_pot()

    def wiper_save(self) -> None:
        # chip select, stand by
        self._cs.value = True

    def _move_wiper(self, steps: int, direction: bool) -> None:
        # set u/d direction
        self._ud.value = direction
        # time.sleep(0.003)
        self._cs.value = False

        # u/d direction means wiper up or down
        cnt = self.max_step if steps > self.max_step else steps
        # toggle pin inc to move the wiper
        for _ in range(cnt):
            self._inc.value = True
            time.sleep(0.001)
            self._inc.value = False
            time.sleep(0.001)

        self._inc.value = True

    def max_pot(self) -> None:
        self._move_wiper(self.max_step + 1, True)

    def min_pot(self) -> None:
        self._move_wiper(self.max_step + 1, False)

    def wiper_up(self, steps: int) -> None:
        self._move_wiper(steps, True)

    def wiper_down(self, steps: int) -> None:
        self._move_wiper(steps, False)

    def wiper_to(self, steps: int) -> None:
        self.min_pot()
        self._move_wiper(steps, True)

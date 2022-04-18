import digitalio, time
from microcontroller import Pin


class X9C:
    def __init__(
        self, cs: Pin = None, inc: Pin = None, ud: Pin = None, max_step: int = 99
    ) -> None:
        self.cs = digitalio.DigitalInOut(cs)  # chip select
        self.inc = digitalio.DigitalInOut(inc)  # increase
        self.ud = digitalio.DigitalInOut(ud)  # up or down

        self.cs.direction = digitalio.Direction.OUTPUT
        self.inc.direction = digitalio.Direction.OUTPUT
        self.ud.direction = digitalio.Direction.OUTPUT

        self.max_step = max_step
        self.crt_step = 0
        self.min_pot(True)

    def deselect_with_saving(self) -> None:
        self.cs.value = True

    def deselect_without_saving(self) -> None:
        self.inc.value = False
        self.cs.value = True
        self.inc.value = True

    def _save(self, saving: bool) -> None:
        if saving:
            self.deselect_with_saving()
        else:
            self.deselect_without_saving()

    def _move_wiper(self, steps: int, direction: bool) -> None:
        cnt = self.max_step if steps > self.max_step else steps
        self.ud.value = direction
        self.cs.value = False
        for _ in range(cnt):
            self.inc.value = False
            time.sleep(0.001)
            self.inc.value = True
            time.sleep(0.001)

        time.sleep(0.1)

    def trim_pot(self, steps: int, saving: bool = False) -> None:
        self.crt_step = steps
        self._move_wiper(self.max_step + 1, False)
        self._move_wiper(steps, True)
        self._save(saving)

    def max_pot(self, saving: bool = False) -> None:
        self.crt_step = self.max_step
        self._move_wiper(self.max_step + 1, True)
        self._save(saving)

    def min_pot(self, saving: bool) -> None:
        self.crt_step = 0
        self._move_wiper(self.max_step + 1, False)
        self._save(saving)

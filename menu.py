from lib.lcd.lcd import LCD

class Menu:
    def __init__(self, lcd: LCD) -> None:
        self.lcd = lcd

    def display(self) -> None:
        self.lcd.home()

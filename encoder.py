import digitalio, rotaryio, board

class Encoder:
    def __init__(self, channelA, channelB, button) -> None:
        # setup ec11 rotary encoder
        # switch channel A&B will change the direction
        self.ec11 = rotaryio.IncrementalEncoder(channelA, channelB) 
        # setup ec11 button
        self.btn = digitalio.DigitalInOut(button)
        self.btn.direction = digitalio.Direction.INPUT
        self.btn.pull = digitalio.Pull.UP
        self.btn_state = False 
        # initialize button position
        self.last_pos = self.ec11.position
        self.counter = 0
    
    def button_pressed(self) -> bool:
        if not self.btn.value and not self.btn_state:
            self.btn_state = True
        if self.btn.value and self.btn_state == True:
            return True
        return False
    
    def posistion_changed(self) -> int:
        current_pos = self.ec11.position
        pos_change = current_pos - self.last_pos
        if pos_change > 0:
            self.rotary_increase()

        if pos_change < 0:
            self.rotary_decrease()

        self.last_pos = current_pos

    def rotary_increase(self) -> None:
        print('rotary increase')

    def rotary_decrease(self) -> None:
        print('rotary decrease')
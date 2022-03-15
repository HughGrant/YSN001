import digitalio, rotaryio, board

class Encoder:
    def __init__(self, channelA, channelB, button) -> None:
        # setup ec11 rotary encoder
        # switch channel A&B will change the direction
        self.ec11 = rotaryio.IncrementalEncoder(channelA, channelB) 
        ec11_last_pos = ec11_counter = self.ec11.position
        # setup ec11 button
        self.btn = digitalio.DigitalInOut(button)
        self.btn.direction = digitalio.Direction.INPUT
        self.btn.pull = digitalio.Pull.UP
        self.btn_state = False 
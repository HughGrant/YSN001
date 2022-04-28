from scale import Scale


class Vibrator:
    def __init__(self, movement: list[int], scale: Scale) -> None:
        self.movement = movement
        self.scale = scale

    def move(self) -> None:
        print("action")

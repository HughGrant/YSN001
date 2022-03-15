try:
    from typing import Any
except ImportError:
    pass

class Menu:
    def __init__(self, name: str, col: int, row: int, value: Any=None) -> None:
        self.name = name
        if value is None:
            self.content = name
        else:
            self.content = name + ": " + str(value)
        self.col = col
        self.row = row
        self.value = value
    
    def update(self, new_value: Any) -> None:
        self.value = new_value
        self.content = self.name + ": " + str(new_value)



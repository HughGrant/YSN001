try:
    from typing import Any, Callable
except ImportError:
    pass

from page import Page

class Menu:
    def __init__(self, name: str, col: int, row: int) -> None:
        self.name = name 
        self.col = col
        self.row = row
        self.value = None
        self.showing_value = None
        self.page: Page = None
        self.update_func: Callable = None
        self.content_func: Callable = None
    
    def update(self) -> None:
        new_val = self.update_func()
        if type(new_val) is tuple:
            self.showing_value, self.value = new_val
        else:
            self.value = new_val
    
    def content(self) -> str:
        if self.showing_value is None:
            return self.content_func(self.name, self.value)
        else:
            return self.content_func(self.name, self.showing_value, self.value)
        



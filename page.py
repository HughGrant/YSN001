try:
    from typing import Any, Callable, List
except ImportError:
    pass

from lib.lcd.lcd import LCD

class Item:
    def __init__(
        self,
        name: str,
        always_refresh: bool = False,
        linkable: bool = False
    ) -> None:
        self.name = name
        self.min_val = 0
        self.max_val = 0
        self.val = None
        self.always_refresh = always_refresh
        self.linkable = linkable
        self.update_func: Callable = None
        self.page = None
    
    def get(self) -> str:
        if self.update_func is None:
            self.val = self.name
        if self.val is None or self.always_refresh:
            self.val = self.update_func()
        return self.val

    def display(self, lcd: LCD):
        if self.get() != self.val:
            lcd.print(self.val)

    
    
class Page:
    def __init__(self, name: str, items: List = []) -> None:
        self.name = name
        self.items = items
        self.displayed = False

    
from screen import Screen
import time

try:
    from typing import Any, Callable, List
except ImportError:
    pass

class Item:
    def __init__(
        self,
        name: str,
        always_refresh: bool = False,
        clickable: bool = False
    ) -> None:
        self.name = name
        self.min_val = 0
        self.max_val = 0
        self.val = None
        self.always_refresh = always_refresh
        self.clickable = clickable
        self.update_func: Callable = None
        self.next_page = None
        self.prev_page = None
    
    def get(self) -> str:
        if self.update_func is None:
            self.val = self.name
        if self.val is None or self.always_refresh:
            self.val = self.update_func()
        return self.val
    
    def display(self, screen: Screen) -> None:
        self.get()
        screen.print(self.val)
     
class Page:
    def __init__(self, name: str, items: List = []) -> None:
        self.name = name
        self.items = items
        self.last_page = None
        self.next_page = None

    def display(self, screen: Screen) -> None:
        for i, item in enumerate(self.items):
            screen.set_cursor_pos(i, 0)
            if isinstance(item, list):
                for m in item:
                    if isinstance(m, Item):
                        m.display(screen)
                    else:
                        screen.print(m)
            if isinstance(item, Item): 
                item.display(screen)
from screen import Screen
import time

try:
    from typing import Any, Callable, List
except ImportError:
    pass

class Element:
    def __init__(self, name: str, always_refresh: bool = False) -> None:
        self.name = name
        self.value = None
        self.always_refresh = always_refresh
        self.update_func: Callable = None
    
    def get(self) -> str:
        if self.update_func is None:
            return "{} update_func error".format(self.name)
        if self.value is None or self.always_refresh:
            self.value = self.update_func()
        return self.value

class Row:
    def __init__(self, name: str, eles: List[Element] = [], always_refresh: bool = False) -> None:
        self.name = name
        self.eles = eles
        self.always_refresh = always_refresh
        self.display_func = None

    def display(self) -> None:
        if self.display_func is None:
            return "{} display_func error".format(self.name)
        return self.display_func([ele.get() for ele in self.eles])
     
class Page:
    def __init__(self, name: str, menus: List[Row] = []) -> None:
        self.name = name
        self.rows: List[Row] = menus
        self.last_page = None
        self.next_page = None

    def display(self, screen: Screen) -> None:
        for i, row in enumerate(self.rows):
            if row.always_refresh:
                screen.clear_row(i)
            screen.set_cursor_pos(i, 0)
            screen.print(row.display())
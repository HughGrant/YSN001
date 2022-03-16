from menu import Menu
from screen import Screen
import time

try:
    from typing import List
except ImportError:
    pass

class Page:
    def __init__(self, name: str, menus: List[Menu] = []) -> None:
        self.name = name
        self.menus: List[Menu] = menus
        self.last_page = None
        self.next_page = None
    
    def display(self, screen: Screen) -> None:
        for m in self.menus:
            screen.set_cursor_pos(m.col, m.row)
            screen.print(m.content)


    # def config(self, menus: List[Menu]) -> None:
    #     self.menus = menus
    
    # def append(self, menu: Menu) -> None:
    #     self.menus.append(menu)

    
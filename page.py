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
        self.x = 0
        self.y = 0
        self.update_func: Callable = None
        self.page = None
    
    def get(self) -> str:
        if not self.update_func is None:
            self.val = self.update_func()
        if self.linkable:
            self.val = self.name
        return self.val

    def display(self, lcd: LCD):
        if self.always_refresh or self.val is None:
            self.x, self.y = lcd.cursor_pos()
            self.get()
            lcd.print(self.val)

    def __repr__(self) -> str:
        return "Item: {}, linkable: {}".format(self.name, self.linkable)
    
    
class Page:
    def __init__(self, name: str, items: List = []) -> None:
        self.name = name
        self.items = items
        self.is_current = False
        self.links: list[Item] = []
    
    def get_links(self):
        if len(self.links) > 0:
            return self.links

        for row in self.items:
            if isinstance(row, list):
                for item in row:
                    if isinstance(item, Item):
                        if item.linkable:
                            self.links.append(item)
            if isinstance(row, Item):
                if row.linkable:
                    self.links.append(row)
        print(self.links)
        return self.links

    


    
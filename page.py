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
        self.page: Page = None
    
    def set_item_pos(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        if self.always_refresh or self.val is None:
            self.val = self.update_func()
        else:
            self.val = self.name

        return self.val
    
        

    def __repr__(self) -> str:
        return "Item: {}, linkable: {}".format(self.name, self.linkable)
    
    
class Page:
    def __init__(self, name: str, items: List = [], need_cursor: bool = False) -> None:
        self.name = name
        self.items = items
        self.need_cursor = need_cursor
        self.links: list[Item] = []

        self.drawed = False
    
    def get_links(self) -> list[Item]:
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
        return self.links

    


    
try:
    from typing import Any, Callable, List
except ImportError:
    pass

from lib.lcd.lcd import LCD

class Item:
    def __init__(
            self,
            name: str,
            x: int = 0,
            y: int = 0,
            need_refresh: bool = False,
            need_cursor: bool = False
        ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.need_refresh = need_refresh
        self.need_cursor = need_cursor 
        self.update_func: Callable = None
        self.link: list[Item] = None
    
    def __str__(self) -> str:
        if self.need_refresh:
            self.val = self.update_func()
            return self.val
        
        if not self.update_func is None:
            self.val = self.update_func()
            return self.val
        
        self.val = self.name
        return self.val
        
    def __repr__(self) -> str:
        return f"Item: {self.name}"
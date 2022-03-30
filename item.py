try:
    from typing import Any, Callable
except ImportError:
    pass

from lib.lcd.lcd import LCD


class Item:
    def __init__(
            self,
            name: str,
            x: int = 0,
            y: int = 0,
            is_config: bool = False,
            need_refresh: bool = False,
            need_cursor: bool = False,
            config_val: Any = 0.0,
            max_display_val: Any = 0.0,
            min_display_val: Any = 0.0,
            step = 0
        ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.is_config = is_config
        self.need_refresh = need_refresh
        self.need_cursor = need_cursor 
        self.config_val = config_val
        self.max_display_val = max_display_val
        self.min_display_val = min_display_val
        self.step: Any = step
        self.page: list[Item] = None
        self.update_func: Callable = None
        self.save_func: Callable = None
    
    def save(self):
        print("saved")

    def __str__(self) -> str:
        if self.is_config and self.need_refresh:
            return self.config_val

        if self.need_refresh:
            self.config_val = self.update_func()
            return self.config_val
        
        if not self.update_func is None:
            self.config_val = self.update_func()
            return self.config_val
        
        self.config_val = self.name
        return self.config_val
        
    def __repr__(self) -> str:
        return f"Item: {self.name}"
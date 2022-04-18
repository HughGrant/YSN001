from lib.lcd.lcd import LCD


class Link:
    def __init__(
            self,
            name: str,
            type: str = "TEXT",
            need_refresh: bool = False,
        ) -> None:
        self.name = name
        self.type = type
        self.need_refresh = need_refresh
        # added attr
        self.config_val = 0
        self.max_display_val = 0
        self.min_display_val = 0
        self.page: list[Link] = None
        self.update_func = None
        self.press_func = None
        self.x = 0
        self.y = 0

    def knob_increase(self) -> None:
        print(self.name)

    def knob_decrease(self) -> None:
        print(self.name)

    def save(self):
        if not self.save_func is None:
            self.save_func(self.config_val)
    
    def __str__(self) -> str:
        if self.type == "CONF" and self.need_refresh:
            return self.config_val

        if self.need_refresh:
            self.config_val = self.update_func()
            return self.config_val
        
        if self.update_func is not None:
            self.config_val = self.update_func()
            return self.config_val
        
        self.config_val = self.name
        return self.config_val

    def __repr__(self) -> str:
        return f"Link {self.name}"

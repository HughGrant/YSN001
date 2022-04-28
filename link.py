from lib.lcd.lcd import LCD


class Link:
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        self.type = type
        # added attr
        self.config_val = 0
        self.max_display_val = 0
        self.min_display_val = 0
        self.page: list[Link] = None
        self.update_func = None
        self.press_func = None
        self.x = 0
        self.y = 0

    def __str__(self) -> str:
        if self.update_func is not None:
            self.config_val = self.update_func()
            return self.config_val

        return self.name

    def __repr__(self) -> str:
        return f"Link {self.name}"

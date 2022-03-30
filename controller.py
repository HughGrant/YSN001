from item import Item

class Controller:
    def __init__(self, crt_page: list[list]) -> None:
        self.crt_page = crt_page
        self.index: int = 0
        self.links: list[Item] = None
        self.refresh_items: list[Item] = None
        self.crt_item: Item = None
        self.filter_items()
    
    def filter_items(self) -> None:
        items = [item for rows in self.crt_page for item in rows if isinstance(item, Item)]
        self.links = [item for item in items if not item.page is None or item.is_config]
        self.refresh_items = [item for item in items if item.need_refresh]
        self.index = 0
        self.crt_item = self.links[self.index]
    
    def increase_setting(self) -> None:
        self.crt_item.config_val += self.crt_item.step
        if self.crt_item.config_val >= self.crt_item.max_display_val:
            self.crt_item.config_val = self.crt_item.max_display_val

    def decrease_setting(self) -> None:
        self.crt_item.config_val -= self.crt_item.step
        if self.crt_item.config_val <= self.crt_item.min_display_val:
            self.crt_item.config_val = self.crt_item.min_display_val
    
    def save_setting(self) -> None:
        self.crt_item.save()

    def move_next_link(self) -> None:
        self.index += 1
        if self.index >= len(self.links):
            self.index = 0
        self.crt_item = self.links[self.index]

    def move_prev_link(self) -> None:
        self.index -= 1
        if self.index < 0:
            self.index = len(self.links) - 1
        self.crt_item = self.links[self.index]

    def link_pressed(self) -> None:
        self.crt_page = self.crt_item.page
        self.filter_items()
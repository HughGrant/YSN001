from link import Link

class Controller:
    def __init__(self, page: list[list]) -> None:
        self.crt_page = page
        self.index: int = 0
        self.links: list[Link] = None
        self.refresh_items: list[Link] = None
        self.crt_item: Link = None
        self.gather_links()
    
    def gather_links(self) -> None:
        self.links = []
        self.refresh_items = []
        for x, rows in enumerate(self.crt_page):
            y = 0
            for item in rows:
                if isinstance(item, Link):
                    item.x = x
                    item.y = y
                    if item.type == "FUNC":
                        self.links.append(item) 
                    if item.need_refresh:
                        self.refresh_items.append(item)
                y += len(str(item))
        # focus cursor to first link 
        self.index = 0
        self.crt_item = self.links[self.index]

    def knob_press(self) -> None:
        if self.crt_item.type == "FUNC":
            self.crt_item.press_func()
        
        if self.crt_item.type == "CONF":
            print("conf name:", self.crt_item.name)

    def knob_increase(self) -> None:
            self.move_next_link()

    def knob_decrease(self) -> None:
            self.move_prev_link()

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

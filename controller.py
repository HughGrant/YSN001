from link import Link


class Controller:
    def __init__(self, page: list[list]) -> None:
        self.crt_page = page
        self.index: int = 0
        self.links: list[Link] = None
        self.refresh_items: list[Link] = None
        self.crt_link: Link = None
        self.gather_links()

    def gather_links(self) -> None:
        self.links = []
        for x, rows in enumerate(self.crt_page):
            y = 0
            for link in rows:
                if isinstance(link, Link):
                    link.x = x
                    link.y = y
                    self.links.append(link)
                y += len(str(link))
        # focus cursor to first link
        self.index = 0
        self.crt_link = self.links[self.index]
        print("all link in crt page")
        print(self.links)

    def knob_press(self) -> None:
        self.crt_link.press_func()

    def increase_setting(self) -> None:
        self.crt_link.config_val += self.crt_link.step
        if self.crt_link.config_val >= self.crt_link.max_display_val:
            self.crt_link.config_val = self.crt_link.max_display_val

    def decrease_setting(self) -> None:
        self.crt_link.config_val -= self.crt_link.step
        if self.crt_link.config_val <= self.crt_link.min_display_val:
            self.crt_link.config_val = self.crt_link.min_display_val

    def save_setting(self) -> None:
        self.crt_link.save()

    def move_next_link(self) -> None:
        self.index += 1
        if self.index >= len(self.links):
            self.index = 0
        self.crt_link = self.links[self.index]

    def move_prev_link(self) -> None:
        self.index -= 1
        if self.index < 0:
            self.index = len(self.links) - 1
        self.crt_link = self.links[self.index]

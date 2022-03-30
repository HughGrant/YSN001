from item import Item

class Controller:
    def __init__(self, page: list[list]) -> None:
        self.page = page
        self.index: int = 0
        self.links: list[Item] = None
        self.refresh_items: list[Item] = None
        self.link: Item = None
        self.make_links()
    
    def make_links(self) -> None:
        items = [item for rows in self.page for item in rows if isinstance(item, Item)]
        self.links = [item for item in items if not item.link is None]
        self.refresh_items = [item for item in items if item.need_refresh]
        self.index = 0
        self.link = self.links[self.index]
    
    def move_next_link(self) -> None:
        self.index += 1
        if self.index >= len(self.links):
            self.index = 0
        self.link = self.links[self.index]

    def move_prev_link(self) -> None:
        self.index -= 1
        if self.index < 0:
            self.index = len(self.links) - 1
        self.link = self.links[self.index]

    def change_page(self) -> None:
        self.page = self.link.link
        self.make_links()
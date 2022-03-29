from page import Item, Page

class Controller:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.init_controll()
    
    def move_next_item(self) -> Item:
        # print("self.crt_index:", self.index, "self.crt_bound:", self.bound)
        self.index += 1
        if self.index >= self.bound:
            self.index = 0
        return self.links[self.index]

    def move_prev_item(self) -> Item:
        # print("self.crt_index:", self.index, "self.crt_bound:", self.bound)
        self.index -= 1
        if self.index < 0:
            self.index = self.bound - 1
        return self.links[self.index]

    def change_page(self) -> Page:
        self.page = self.links[self.index].page
        self.init_controll()
        return self.page

    def init_controll(self) -> None:
        # get all links and reconfig this controller with the new page
        self.page.get_links()
        self.index = 0
        self.links = self.page.links
        self.bound = len(self.links)
        self.crt_item = self.links[0]
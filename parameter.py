import struct
from lib.nvm import nvm_helper

try:
    from typing import Any
except ImportError:
    pass

OFFSET = 'OFFSET'
SCALAR = 'SCALAR'
MAX_WEIGHT = 'MAX_WEIGHT'
CURRENT_CNT = 'CURRENT_CNT'
MAX_CNT = 'MAX_CNT'
MAX_DISPLAY_CNT = "MAX_DISPLAY_CNT"

class Setting:

    def __init__(self) -> None:
        self.defaults = {
            OFFSET: 95700,
            SCALAR: 700,
            MAX_WEIGHT: 500,
            CURRENT_CNT: 0,
            MAX_CNT: 99999,
            MAX_DISPLAY_CNT: 99999,
        }
        self.cache = nvm_helper.read_data()

    def get(self, name: str) -> Any:
        return self.cache.get(name, self.defaults[name])

    def save(self, name: str, val: Any) -> None:
        # rom = nvm_helper.read_data()
        self.cache.update({name: val})

    def write(self) -> None:
        # only writes to the flash when needed
        nvm_helper.save_data(self.cache, False)

    def print_settings(self) -> None:
        print(self.cache)
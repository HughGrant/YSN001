import struct
from lib.nvm import nvm_helper

try:
    from typing import Any
except ImportError:
    pass

DEBUG = True
OFFSET = 'OFFSET'
FACTOR = 'FACTOR'
MAX_WEIGHT = 'MAX_WEIGHT'
CURRENT_CNT = 'CURRENT_CNT'
MAX_CNT = 'MAX_CNT'

class Setting:
    def __init__(self) -> None:
        # Global methods for read or write data
        self.defaults = {
            OFFSET: 95700,
            FACTOR: 700,
            MAX_WEIGHT: 500,
            CURRENT_CNT: 0,
            MAX_CNT: 9999,
        }
        self.cache = nvm_helper.read_data()

    def get(self, name: str) -> Any:
        if DEBUG:
            print("cache get '{}' called".format(name))
        return self.cache.get(name, self.defaults[name])

    def save(self, name: str, val: Any) -> None:
        # rom = nvm_helper.read_data()
        self.cache.update({name: val})
        if DEBUG:
            print("rom set '{}': {} called".format(name, val))
    
    def write(self) -> None:
        # only writes to the flash when needed
        nvm_helper.save_data(self.cache, False)
        if DEBUG:
            print("actual writing to the flash")
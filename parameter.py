from lib.nvm import nvm_helper

try:
    from typing import Any
except ImportError:
    pass

# Global methods for read or write data
defaults = {
    'OFFSET': 95700,
    'FACTOR': 700,
}

def get(name: str) -> Any:
    rom = nvm_helper.read_data()
    return rom.get(name, defaults[name])

def write(name: str, new_val: Any) -> None:
    rom = nvm_helper.read_data()
    rom.update({name: new_val})
    nvm_helper.save_data(rom, False)
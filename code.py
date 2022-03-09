import board
import digitalio
import time
import busio
from lib.lcd.lcd import LCD
from lib.lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lib.lcd.lcd import CursorMode
from lib.hx711.hx711_gpio import HX711

# setup board led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
# setup i2c for lcd display
i2c = busio.I2C(board.GP1, board.GP0)
# setup for hx711
pin_dt = digitalio.DigitalInOut(board.GP15)
pin_sck = digitalio.DigitalInOut(board.GP14)
pin_sck.direction = digitalio.Direction.OUTPUT
# initialize load cell
hx = HX711(pin_sck, pin_dt)
hx.tare()

#blink the board LED if i2c lock cannot be accquired
while not i2c.try_lock():
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)

try:
    address = i2c.scan()[0]
    print("i2c address for lcd:", hex(address))
finally:
    i2c.unlock()

# default size for the interface:  20x4x8
lcd = LCD(I2CPCF8574Interface(i2c, address))
lcd.print("LCD Initialize Done")

#Display Menu
#Calibrate Load Cell

while True:
    data = hx.get_value()
    print("data:", data)
    time.sleep(0.2)
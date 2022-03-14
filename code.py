import board
import rotaryio
import digitalio
import time
import busio
from lib.lcd.lcd import LCD
from lib.lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lib.hx711.hx711_gpio import HX711
from lib.lcd.lcd import CursorMode


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
time.sleep(0.5)
hx.set_scale(700)
hx.tare()

# setup ec11 rotary encoder
# switch channel A&B will change the direction
ec11_encoder = rotaryio.IncrementalEncoder(board.GP4, board.GP3) 
ec11_last_pos = ec11_counter = ec11_encoder.position
# setup ec11 button
ec11_btn = digitalio.DigitalInOut(board.GP2)
ec11_btn.direction = digitalio.Direction.INPUT
ec11_btn.pull = digitalio.Pull.UP
ec11_btn_state = False 

#blink the board LED if i2c lock cannot be accquired
# while not i2c.try_lock():
#     led.value = True
#     time.sleep(0.5)
#     led.value = False
#     time.sleep(0.5)

# try:
#     address = i2c.scan()[0]
#     print("i2c address for lcd:", hex(address))
# finally:
#     i2c.unlock()

# default size for the interface: 20x4x8
# default I2C address: o0x27
lcd = LCD(I2CPCF8574Interface(i2c, 0x27))

#Display Menu
#Calibrate Load Cell

while True:
    lcd.home()
    lcd.print("Read Value: " + str(hx.last_val))
    lcd.set_cursor_pos(1, 0)
    lcd.print("OFFSET:" + str(hx.OFFSET))
    lcd.set_cursor_pos(2, 0)
    lcd.print("SCALE:" + str(hx.SCALE))
    ec11_current_pos = ec11_encoder.position
    pos_change = ec11_current_pos - ec11_last_pos
    if pos_change > 0:
        hx.SCALE = hx.SCALE + 10

    if pos_change < 0:
        hx.SCALE = hx.SCALE - 10

    ec11_last_pos = ec11_current_pos

    if not ec11_btn.value and not ec11_btn_state:
        ec11_btn_state = True
    if ec11_btn.value and ec11_btn_state == True:
        lcd.set_cursor_pos(0, 0)
        lcd.print("Tare, please wait")
        hx.tare(30)
        lcd.clear()
        ec11_btn_state = False

    weight = hx.get_round_units()
    lcd.set_cursor_pos(3, 0)
    lcd.print("Weight: " + str(weight))
    # lcd.set_cursor_pos(3, 19)
    # lcd.set_cursor_mode(CursorMode.LINE)
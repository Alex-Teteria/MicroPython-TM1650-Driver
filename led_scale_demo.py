from machine import I2C
from ky040_encoder import RotaryEncoder
from tm1650 import TM1650
import time


# init LED scale
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=100_000)
disp = TM1650(i2c)
# brightness level (1..8), max level 8
disp.set_brightness(8)

# init encoder ky040
r = RotaryEncoder(clk_pin=14,
                  dt_pin=15,
                  debounce_ms=5,
                  callback= lambda pos, direction: rotary_event(pos, 31, wrap=False)
                  )
# pin for switching modes
pin_mode = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)

def rotary_event(pos, val_max, wrap=True):
    '''callback for RotaryEncoder()
       val_max - (int), max value for RotaryEncoder.position
    '''
    # mode WRAP
    if wrap:
        pos %= val_max
    # mode BOUNDED
    else:
        if r.position > val_max-1:
            r.position = val_max-1
        elif r.position < 1:
            r.position = 1
        if pos > val_max-1:
            pos = val_max-1
    disp.show_num_on_scale(pos, fill=mode)
    print("Position:", pos)

def debounce_pin(pin, num_delay):
    ''' вертає True, коли pin в стані "0"
        num_delay - множник для визначення затримки, затримка = num_delay * 10mc  
    '''
    if not pin.value(): 
        for i in range(num_delay):
            time.sleep_ms(10)
            if pin.value():
                break
        else:
            return True
    return False


disp.clear()
# start position:
r.position = 0
mode = 1 # scale mode (WRAP or BOUNDED)
while True:
    if debounce_pin(pin_mode, 20):
        while not pin_mode.value():
            pass
        mode = not mode

        
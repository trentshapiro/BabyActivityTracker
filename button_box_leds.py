from machine import Pin
import gc
import time
import secrets

# enable garbage collection
gc.enable()

# map buttons and leds
buttons = list([Pin(i, Pin.IN, Pin.PULL_UP) for i in range(0,8)])
leds = list([Pin(i, Pin.OUT, value=0) for i in range(8,16)])
button_default_value = 1
board_led = Pin('LED', Pin.OUT)
board_led.off()

#start timers
current_time = time.localtime()
timer = time.time()
reset_flag = 0

while True:
    if any([button.value()!=button_default_value for button in buttons]):
        high_buttons = [idx for idx,button in enumerate(buttons) if button.value()!=button_default_value]
        [leds[button].value(1-leds[button].value()) for button in high_buttons]
        time.sleep(0.25)
    
    # Check every 5 minutes
    if(time.time() - timer >= 300):
        current_time = time.localtime()
        timer = time.time()
        # Reset at 1am, flag for if interval is hit twice
        if current_time[3] == 1 and current_time[4] > 0 and current_time[4] < 10 and reset_flag == 0:
            [led.value(0) for led in leds]
            reset_flag = 1
        
        reset_flag = 0




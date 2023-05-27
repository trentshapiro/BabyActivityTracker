from machine import Pin
import gc
import time

# enable garbage collection
gc.enable()

# map buttons and leds
buttons = list([Pin(i, Pin.IN, Pin.PULL_UP) for i in range(0,8)])
leds = list([Pin(i, Pin.OUT, value=0) for i in range(8,16)])
button_default_value = 1
board_led = Pin('LED', Pin.OUT)
board_led.off()


while True:
    if any([button.value()!=button_default_value for button in buttons]):
        high_buttons = [idx for idx,button in enumerate(buttons) if button.value()!=button_default_value]
        [leds[button].value(1-leds[button].value()) for button in high_buttons]
        time.sleep(0.25)

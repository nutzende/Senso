from machine import Pin
import machine, neopixel

np = neopixel.NeoPixel(machine.Pin(22), 4)

# Buttons
b_green = Pin(32, Pin.IN, Pin.PULL_DOWN)     #1
b_red = Pin(26, Pin.IN, Pin.PULL_DOWN)       #2
b_yellow = Pin(33, Pin.IN, Pin.PULL_DOWN)    #3
b_blue = Pin(25, Pin.IN, Pin.PULL_DOWN)      #4

#reset
#def handle_interrupt(pin):
#  machine.reset()
#res = Pin(25, Pin.IN, Pin.PULL_DOWN)
#res.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
from machine import Pin

# LEDs
l_green = Pin(21, Pin.OUT)
l_red = Pin(20, Pin.OUT)
l_yellow = Pin(22, Pin.OUT)
l_blue = Pin(19, Pin.OUT)

#Neopixel
l_neo = Pin(15, Pin.OUT)

# Buttons
b_green = Pin(32, Pin.IN, Pin.PULL_DOWN)     #1
b_red = Pin(33, Pin.IN, Pin.PULL_DOWN)       #2
b_yellow = Pin(26, Pin.IN, Pin.PULL_DOWN)    #3
b_blue = Pin(25, Pin.IN, Pin.PULL_DOWN)      #4


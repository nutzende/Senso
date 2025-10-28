from machine import Pin, SoftI2C
import ssd1306
import time, random

# Log Ausgabe / Start Animation / Display
dev = True
st_ani = False
display = True

# LEDs
l_green = Pin(21, Pin.OUT)    #32
l_red = Pin(22, Pin.OUT)      #26
l_yellow = Pin(20, Pin.OUT)   #27
l_blue = Pin(19, Pin.OUT)     #25

# Buttons
b_green = Pin(33, Pin.IN, Pin.PULL_DOWN)     #1 #9
b_red = Pin(26, Pin.IN, Pin.PULL_DOWN)       #2 #22
b_yellow = Pin(32, Pin.IN, Pin.PULL_DOWN)    #3 #33
b_blue = Pin(25, Pin.IN, Pin.PULL_DOWN)      #4 #15

if display == True:
    from machine import SoftI2C
    i2c = SoftI2C(scl=Pin(7), sda=Pin(8))
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.fill(0)
    
# Variablen
sequence = []        # Liste mit bisherigen Farben
player_index = 0     # Fortschritt beim Nachdrücken
seq_index = 0
runde = 0
led_timer = 0
led_on = False
run_game = 0
last_press_time = 0
now = 0
texthoehe = 0

# Debug Funktion
def log(msg):
    if dev:
        if display == True:
            global texthoehe
            if texthoehe >= 60:
                texthoehe = 0
                oled.fill(0)
            oled.text(msg, 0, texthoehe)
            oled.show()
            texthoehe = texthoehe + 10
        else:
            #time = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
            print(msg)




# Beispielhafte Bitmaps (du kannst sie schöner gestalten)
font_umlaute = {
    'ä': [
        0b01001000,
        0b00000000,
        0b01110000,
        0b00001000,
        0b01111000,
        0b10001000,
        0b01111000,
        0b00000000
    ],
    'ö': [
        0b01001000,
        0b00000000,
        0b01110000,
        0b10001000,
        0b10001000,
        0b01110000,
        0b00000000,
        0b00000000
    ],
    'ü': [
        0b01001000,
        0b00000000,
        0b10001000,
        0b10001000,
        0b10001000,
        0b01111000,
        0b00000000,
        0b00000000
    ],
    'ß': [
        0b01110000,
        0b10001000,
        0b10000000,
        0b11100000,
        0b10001000,
        0b10001000,
        0b11110000,
        0b00000000
    ]
}

CHAR_WIDTH = 8
CHAR_HEIGHT = 8
def draw_char(x, y, bitmap):
    for row, byte in enumerate(bitmap):
        for col in range(8):
            if byte & (1 << (7 - col)):
                oled.pixel(x + col, y + row, 1)
                
def draw_text_with_umlauts(oled, text, x, y):
    pos_x = x
    for ch in text:
        if ch in font_umlaute:
            draw_char(pos_x, y, font_umlaute[ch])
        else:
            oled.text(ch, pos_x, y)
        pos_x += CHAR_WIDTH  # Nächste Position um 8 Pixel verschieben


oled.fill(0)
draw_text_with_umlauts(oled, "Toll: ö ä ü !", 0, 0)
oled.show()
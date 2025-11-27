from machine import Pin, I2C
import ssd1309
i2c = I2C(0, scl=Pin(7), sda=Pin(8))
oled_width = 128
oled_height = 64
oled = ssd1309.Display(i2c=i2c, width=128, height=64)
oled.clear()
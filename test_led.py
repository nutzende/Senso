from machine import Pin
import ssd1306
import time

display = True #Display Ja/Nein
if display == True:
    from machine import SoftI2C
    i2c = SoftI2C(scl=Pin(7), sda=Pin(8))
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.fill(0)
    
def log(text):
    if display == True: #Zeige Log auf dem Display wenn angeschlossen
        global texthoehe
        if texthoehe >= 60:
            texthoehe = 0
            oled.fill(0)
        oled.text(text, 0, texthoehe)
        oled.show()
        texthoehe = texthoehe + 10
    else:
        print(text) # Wenn kein Display angeschlossen -> Consolen Output
        
texthoehe = 0
led_gruen = Pin(21, Pin.OUT)
led_gelb = Pin(20, Pin.OUT)
led_rot = Pin(22, Pin.OUT)
led_blau = Pin(19, Pin.OUT)

taster_gruen = Pin(33, Pin.IN)
taster_gelb = Pin(32, Pin.IN)
taster_rot = Pin(26, Pin.IN)
taster_blau = Pin(25, Pin.IN)

led_gruen.value(0)
led_gelb.value(0)
led_rot.value(0)
led_blau.value(0)
blinkinprogress = 0

def blinktest():
    global blinkinprogress
    blinkinprogress = 1
    time.sleep(1)
    led_gruen.value(1)
    time.sleep(0.25)
    led_gelb.value(1)
    time.sleep(0.25)
    led_rot.value(1)
    time.sleep(0.25)
    led_blau.value(1)
    time.sleep(1)
    led_gruen.value(0)
    time.sleep(0.25)
    led_gelb.value(0)
    time.sleep(0.25)
    led_rot.value(0)
    time.sleep(0.25)
    led_blau.value(0)
    blinkinprogress = 0
    log('blicken fertig')


while True:
    if blinkinprogress == 0 and (taster_gruen.value() == 1 or taster_gelb.value() == 1 or taster_rot.value() == 1 or taster_blau.value() == 1):
        #print("Taster Gruen: ",taster_gruen.value())
        log(f"Taster Gruen: {taster_gruen.value()}")
        #print("Taster Gelb: ",taster_gelb.value())
        log(f"Taster Gelb: {taster_gelb.value()}")
        #print("Taster Rot: ",taster_rot.value())
        log(f"Taster Rot: {taster_rot.value()}")
        #print("Taster Blau: ",taster_blau.value())
        log(f"Taster Blau: {taster_blau.value()}")
        blinktest()
        time.sleep(0.2)
        
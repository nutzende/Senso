import time, pin, display as d

display = True #Display Ja/Nein

def log(text):
    if display == True: #Zeige Log auf dem Display wenn angeschlossen
        global texthoehe
        if texthoehe >= 60:
            texthoehe = 0
            d.oled.fill(0)
        d.oled.text(text, 0, texthoehe)
        d.oled.show()
        texthoehe = texthoehe + 10
    else:
        print(text) # Wenn kein Display angeschlossen -> Consolen Output
        
texthoehe = 0

pin.l_green.value(0)
pin.l_yellow.value(0)
pin.l_red.value(0)
pin.l_blue.value(0)
blinkinprogress = 0

def blinktest():
    global blinkinprogress
    blinkinprogress = 1
    time.sleep(1)
    pin.l_blue.value(1)
    time.sleep(0.25)
    pin.l_yellow.value(1)
    time.sleep(0.25)
    pin.l_green.value(1)
    time.sleep(0.25)
    pin.l_red.value(1)
    time.sleep(1)
    pin.l_blue.value(0)
    time.sleep(0.25)
    pin.l_yellow.value(0)
    time.sleep(0.25)
    pin.l_green.value(0)
    time.sleep(0.25)
    pin.l_red.value(0)
    blinkinprogress = 0
    log('blicken fertig')


while True:
    if blinkinprogress == 0 and (pin.b_green.value() == 1 or pin.b_yellow.value() == 1 or pin.b_red.value() == 1 or pin.b_blue.value() == 1):
        #print("Taster Gruen: ",b_green.value())
        log(f"Taster Gruen: {pin.b_green.value()}")
        #print("Taster Gelb: ",b_yellow.value())
        log(f"Taster Gelb: {pin.b_yellow.value()}")
        #print("Taster Rot: ",b_red.value())
        log(f"Taster Rot: {pin.b_red.value()}")
        #print("Taster Blau: ",b_blue.value())
        log(f"Taster Blau: {pin.b_blue.value()}")
        blinktest()
        time.sleep(0.2)
        
import time, random, menu, pin, display

logondisplay = True
# LED Funktionen
def leds_off():
    pin.l_green.off()
    pin.l_red.off()
    pin.l_yellow.off()
    pin.l_blue.off()

def led(num):
    leds_off()
    if num == 1: pin.l_green.on()
    elif num == 2: pin.l_red.on()
    elif num == 3: pin.l_yellow.on()
    elif num == 4: pin.l_blue.on()

def spielerLeds(a):
    x = [1,2,4,3]

    for i in range(4-a):
        x.pop()
    return x

def spiel2(spieler):
    menu.log("Spiel2")
    spieler=spieler
    spielerLed = spielerLeds(spieler)
    aufgaben = ("Mache zehn Liegestützen","Laufe einen Marathon","Erzähle einen Witz")
    menu.log("Zum Starten eine beliebige Taste drücken")
    
    if menu.read_button(0)>0:
            
    while True:
        ausgwSpieler = random.randint(1,spieler)
        for i in range(50+ausgwSpieler):
            led(spielerLed[i%spieler])
            time.sleep(0.0001*((i-25)*(i-25))+0.05)
            if i+1 == ausgwSpieler+50:
                menu.log(aufgaben[random.randint(0,2)])
                time.sleep(3)
                leds_off()
                menu.log("Zum weiter Spielen blau drücken, zum Abbrechen rot drücken")
        button = 0
        while button not 4 or button not 2:
            button = menu.read_button(0) 
        if button==4:
            spiel2(spieler)
        elif button==2:
            break
            

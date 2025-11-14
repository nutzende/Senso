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
def pre_start_flaschendrehen():
    menu.menu_ui.init_menu()
    menu.menutext("Set players", "title", "title", 0)
    menu.menutext("2 Players", "text", 1, 0)
    menu.menutext("3 Players", "text", 2, 0)
    menu.menutext("4 Players", "text", 3, 0)
    eingabe = menu.read_button(0)
    if eingabe == 1:
        spiel2(2)
    elif eingabe == 2:
        spiel2(3)
    elif eingabe == 3:
        spiel2(4)
    else:
        pre_start_flaschendrehen()
def spiel2(spieler):
    menu.log("Spiel2")
    spieler=spieler
    spielerLed = spielerLeds(spieler)
    aufgaben = ("Mache zehn Liegestützen","Laufe einen Marathon","Erzähle einen Witz")
    menu.cleardisplay()
    menu.menutext("Zum Starten", "center", "top", 0)
    menu.menutext("eine beliebige", "center", "center", 0)
    menu.menutext("Taste drücken", "center", "bottom", 0)
    
    if menu.read_button(0)>0:
        menu.cleardisplay()
        display.oled.show()
        while True:
            ausgwSpieler = random.randint(1,spieler)
            for i in range(50+ausgwSpieler):
                led(spielerLed[i%spieler])
                time.sleep(0.0001*((i-25)*(i-25))+0.05)
                if i+1 == ausgwSpieler+50:
                    menu.log(aufgaben[random.randint(0,2)])
                    time.sleep(3)
                    leds_off()
                    menu.menutext("Neuer Versuch?", "center", "top", 0)
                    menu.menutext("Blau: Ja", "center", "center", 0)
                    menu.menutext("Rot: Nein", "center", "bottom", 0)
            button = 0
            while button != 4 or button != 2:
                button = menu.read_button(0)
                print(button)
                if button==4:
                    spiel2(spieler)
                elif button==2:
                    break
            break
        menu.cleardisplay()
        menu.mainmenu()
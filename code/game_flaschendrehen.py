import time, random, menu, pin, display

logondisplay = True

# LED Funktionen
def leds_off():
    pin.np[0] = (0,0,0)
    pin.np[1] = (0,0,0)
    pin.np[2] = (0,0,0)
    pin.np[3] = (0,0,0)
    pin.np.write()

def led(num):
    leds_off()
    if num == 1: pin.np[2] = (0,0,255)
    elif num == 2: pin.np[1] = (255,0,0)
    elif num == 3: pin.np[0] = (0,255,0)
    elif num == 4: pin.np[3] = (255,255,0)
    pin.np.write()

def spielerLeds(a):
    x = [1,2,3,4]

    for i in range(4-a):
        x.pop()
    return x

# Button lesen
def read_button():
    if pin.b_blue.value(): return 1
    if pin.b_red.value(): return 2
    if pin.b_green.value(): return 3
    if pin.b_yellow.value(): return 4
    return 0

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
def aufgaben(n):
    menu.cleardisplay()
    if n == 0:
        menu.menutext("Keine Aufgabe", "center", "top", 0)
    elif n == 1:
        menu.menutext("Mache zehn", "center", "top", 0)
        menu.menutext("Liegestützen", "center", "center", 0)
    elif n == 2:
        menu.menutext("Laufe einen", "center", "top", 0)
        menu.menutext("Marathon", "center", "center", 0)
def spiel2(spieler):
    menu.log("Spiel2")
    spieler=spieler
    spielerLed = spielerLeds(spieler)
    menu.cleardisplay()
    while read_button() > 0:
            menu.log("Button pressed")
            time.sleep(0.25)
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
                    aufgaben(random.randint(0,2))
                    time.sleep(3)
                    menu.cleardisplay()
                    leds_off()
                    menu.menu_ui.init_menu()
                    menu.menutext("Neuer Versuch", "title", "title", 0)
                    menu.menutext("Nein", "text", 2, 0)
                    menu.menutext("Ja", "text", 3, 0)
            button = 0
            while button != 3 or button != 2:
                button = menu.read_button(0)
                print(button)
                if button==3:
                    spiel2(spieler)
                elif button==2:
                    break
            break
        menu.cleardisplay()
        menu.mainmenu()
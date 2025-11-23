import time, random, pin, menu

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

def read_button():
    if pin.b_green.value(): return 1
    if pin.b_red.value(): return 2
    if pin.b_yellow.value(): return 3
    if pin.b_blue.value(): return 4
    return 0

def read_button_msec(msec):
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_add(start, msec ), time.ticks_ms()) > 0 or msec == 0:
        if pin.b_green.value(): return 1
        if pin.b_red.value(): return 2
        if pin.b_yellow.value(): return 3
        if pin.b_blue.value(): return 4
    return 0

def whacamole(lvl):
    while read_button() > 0:
        print("Button pressed")
        time.sleep(0.2)
    print("Zum Starten beliebigen Knopf drücken")
    menu.menutext("Zum Starten", "center", "top", 0)
    menu.menutext("beliebigen Knopf", "center", "center", 0)
    menu.menutext("drücken", "center", "bottom", 0)
    read_button_msec(0)
    time.sleep(0.2)
    abbr = False
    for i in range(lvl):
        menu.cleardisplay()
        menu.menutext(f"Runde: {i+1}", "center", "top", 0)
        print("Runde:", i+1)  
        for j in range(4):
            mole = random.randint(1,4)
            led(mole)
            if read_button_msec(2150-(i*200)) != mole:
                menu.menutext("Verloren", "center", "center", 0)
                print("Verloren")
                leds_off()
                time.sleep(0.2)
                abbr = True
                break
            else:
                leds_off()
                time.sleep(0.2)
                print("richtig")
        if abbr: break
    if not abbr:
        print("Gewonnen!")
        menu.menutext("Gewonnen!", "center", "center", 0)
    time.sleep(3)
    menu.cleardisplay()
    menu.menutext("Neuer Versuch?", "center", "top", 0)
    menu.menutext("Gruen: Ja", "center", "center", 0)
    menu.menutext("Rot: Nein", "center", "bottom", 0)
    eingabe = menu.read_button(0)
    menu.cleardisplay()
    if eingabe == 1:
        whacamole(2)
    if eingabe == 2:
        menu.menutext("zurueck Menue", "center", "center", 1)
        menu.cleardisplay()
        menu.mainmenu()
    else:
        menu.menutext("Falsche Eingabe", "center", "top", 0)
        menu.menutext("zurueck Menue", "center", "center", 1)
        menu.cleardisplay()
        menu.mainmenu()
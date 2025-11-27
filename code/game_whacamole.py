import time, random, pin, menu

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
    elif num == 2: pin.np[3] = (255,255,0)
    elif num == 3: pin.np[0] = (0,255,0)
    elif num == 4: pin.np[1] = (255,0,0)
    pin.np.write()

# Button lesen
def read_button():
    if pin.b_blue.value(): return 1
    if pin.b_yellow.value(): return 2
    if pin.b_green.value(): return 3
    if pin.b_red.value(): return 4
    return 0

def read_button_msec(msec):
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_add(start, msec ), time.ticks_ms()) > 0 or msec == 0:
        if pin.b_blue.value(): return 1
        if pin.b_yellow.value(): return 2
        if pin.b_green.value(): return 3
        if pin.b_red.value(): return 4
    return 0

def pre_start_whacamole():
    menu.menu_ui.init_menu()
    menu.menutext("Set Gamemode", "title", "title", 0)
    menu.menutext("Leicht", "text", 1, 0)
    menu.menutext("Mittel", "text", 2, 0)
    menu.menutext("Schwer", "text", 3, 0)
    eingabe = menu.read_button(0)
    menu.cleardisplay()
    if eingabe == 1:
        whacamole(3)
    elif eingabe == 2:
        whacamole(6)
    elif eingabe == 3:
        whacamole(9)
    else:
        pre_start_whacamole()

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
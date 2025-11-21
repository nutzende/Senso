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
    if num == 1: pin.np[1] = (0,255,0)
    elif num == 2: pin.np[0] = (255,0,0)
    elif num == 3: pin.np[2] = (255,255,0)
    elif num == 4: pin.np[3] = (0,0,255)
    pin.np.write()

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

def pre_start_reaction():
    menu.menu_ui.init_menu()
    menu.menutext("LED Rotation", "title", "title", 0)
    menu.menutext("Leicht", "text", 1, 0)
    menu.menutext("Mittel", "text", 2, 0)
    menu.menutext("Schwer", "text", 3, 0)

    eingabe = menu.read_button(0)
    menu.cleardisplay()

    if eingabe == 1:
        reaction(4)
    elif eingabe == 2:
        reaction(7)
    elif eingabe == 3:
        reaction(10)
    else:
        pre_start_reaction()

def reaction(levels):
    # Warten bis Spieler bereit
    while read_button() > 0:
        time.sleep(0.2)
    menu.menutext("Zum Starten", "center", "top", 0)
    menu.menutext("beliebigen Knopf", "center", "center", 0)
    menu.menutext("drücken", "center", "bottom", 0)
    read_button_msec(0)
    time.sleep(0.2)
    lives = 3
    for lvl in range(levels):
        menu.cleardisplay()
        menu.menutext(f"Runde {lvl+1}", "center", "top", 0)
        menu.menutext(f"Leben: {lives}", "center", "center", 0)
        print("Runde:", lvl+1)
        delay = 350 - (lvl * 25)
        if delay < 80:
            delay = 80
        for n in range(1, 5):
            led(n)
            pressed = read_button_msec(delay)
            if n == 2:
                if pressed != 2:
                    lives -= 1
                    print("Fehler! Falsches Timing.")
            else:
                if pressed != 0:
                    lives -= 1
                    print("Fehler! Knopf zu früh gedrückt.")

            leds_off()
            if lives <= 0:
                break

        if lives <= 0:
            break
        time.sleep(0.2)
        
    if lives <= 0:
        menu.menutext("VERLOREN!", "center", "center", 0)
        print("Verloren!")
    else:
        menu.menutext("GEWONNEN!", "center", "center", 0)
        print("Gewonnen!")

    time.sleep(3)
    menu.cleardisplay()
    menu.menutext("Neuer Versuch?", "center", "top", 0)
    menu.menutext("Gruen: Ja", "center", "center", 0)
    menu.menutext("Rot: Nein", "center", "bottom", 0)
    eingabe = menu.read_button(0)
    menu.cleardisplay()
    if eingabe == 1:
        reaction(3)
    elif eingabe == 2:
        menu.mainmenu()
    else:
        menu.mainmenu()
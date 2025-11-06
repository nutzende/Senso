import time, pin, display as d

show_display = True   
logondisplay = False
dev = True
texthoehe = 0
import game_senso
# Error Log
def log(msg):
    global texthoehe
    if dev:
        if logondisplay:
            if texthoehe >= 60:
                texthoehe = 0
                d.oled.fill(0)
            d.oled.text(msg, 0, texthoehe)
            d.oled.show()
            texthoehe += 10
        else:
            print(msg)

def cleardisplay():
    d.oled.fill(0)

# Zeitdifferenz in ms
def differenz(ende):
    now = time.ticks_ms()
    ms = ende * 1000
    deadline = time.ticks_add(now, ms)
    return time.ticks_diff(deadline, now)

# Button-Abfrage
def read_button(sec):
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_add(start, sec * 1000), time.ticks_ms()) > 0 or sec == 0:
        if pin.b_green.value(): return 1
        if pin.b_red.value(): return 2
        if pin.b_yellow.value(): return 3
        if pin.b_blue.value(): return 4
    menutext("Zeit abgelaufen", "center", "center", 2)
    return 0

# Menütext anzeigen
def menutext(msg, xpos, ypos, sec=None):
    if show_display:
        error = False
        texthoehe = 8
        # X-Position
        if xpos == "left":
            x_display = 0
        elif xpos == "center":
            x_display = (d.oled_width // 2) - ((len(msg) * 8) // 2)
        elif xpos == "right":
            x_display = d.oled_width - (len(msg) * 8)
        else:
            log("Falsche/Keine Breite übergeben")
            error = True

        # Y-Position
        if ypos == "top":
            y_display = 0
        elif ypos == "center":
            y_display = (d.oled_height // 2) - (texthoehe // 2)
        elif ypos == "bottom":
            y_display = d.oled_height - texthoehe
        else:
            log("Falsche/Keine Höhe übergeben")
            error = True

        if sec is None:
            log(f"Keine Zeit übergeben: {sec}")
            sec = 3
        if not error:
            #d.oled.fill(0)
            d.oled.text(msg, x_display, y_display)
            d.oled.show()
            time.sleep(sec)
        else:
            log("Error")
    else:
        print(msg)

def mainmenu():
    cleardisplay()
    # --- Ablauf ---
    menutext("Spielauswahl", "center", "top", 0)
    menutext("Senso: Blau", "center", "center", 0)
    menutext("Flaschen: Gelb", "center", "bottom", 0)
    eingabe = read_button(0)
    cleardisplay()
    if eingabe > 0:
        for p in ["", ".", "..", "..."]:
            menutext(f"Spiel startet{p}", "center", "center", 0.5)
            cleardisplay()
        if eingabe == 4:
            game_senso.pre_start_senso()
        if eingabe == 3:
            import game_flaschendrehen
            game_flaschendrehen.spiel2(4)
    else:
        menutext("Falsche Eingabe", "center", "center", 1)
        mainmenu()
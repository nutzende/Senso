import time, random, pin, display as d, menu, skilllevel
# Log Ausgabe / Start Animation / Display
dev = True
st_ani = False
display = False

# Variablen
sequence = []        # Liste mit bisherigen Farben
player_index = 0     # Fortschritt beim Nachdrücken
seq_index = 0
runde = 0
led_timer = 0
led_on = False
run_game = 0         #direkter Start nach Menü
last_press_time = 0
now = 0
texthoehe = 0
gamemode = 0
players = 0
selected_player = 0
numspieler = 0
#skilllevel.set_skilllevel(0)
#skill_level = 0      #Skill level 1-4

# Debug Funktion
def log(msg):
    if dev:
        if display == True:
            global texthoehe
            if texthoehe == 0:
                menu.cleardisplay()
            if texthoehe >= 60:
                texthoehe = 0
                menu.cleardisplay()
            d.oled.text(msg, 0, texthoehe)
            d.oled.show()
            texthoehe = texthoehe + 10
        else:
            #time = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
            print(msg)

# LED Funktionen
def leds_off():
    pin.np[0] = (0,0,0)
    pin.np[1] = (0,0,0)
    pin.np[2] = (0,0,0)
    pin.np[3] = (0,0,0)
    pin.np.write()

def all_led():
    pin.np[2] = (0,0,255)
    pin.np[3] = (255,255,0)
    pin.np[0] = (0,255,0)
    pin.np[1] = (255,0,0)
    pin.np.write()

def led(num):
    leds_off()
    if num == 1: pin.np[2] = (0,0,255)
    elif num == 2: pin.np[1] = (255,0,0)
    elif num == 3: pin.np[0] = (0,255,0)
    elif num == 4: pin.np[3] = (255,255,0)
    pin.np.write()

# Button lesen
def read_button():
    if pin.b_blue.value(): return 1
    if pin.b_red.value(): return 2
    if pin.b_green.value(): return 3
    if pin.b_yellow.value(): return 4
    return 0

def start_animation():
    global now, led_timer, led_on
    # Blitz an
    if not led_on and time.ticks_diff(now, led_timer) >= 0:
        leds_off()
        for x in range(4):
            led(random.randint(1, 4))  # zufällige LED "blitzt"
        led_on = True
        led_timer = now + random.randint(50, 150)  # Blitzdauer (50–150 ms)
    
    # Blitz aus + Pause vor nächstem Blitz
    elif led_on and time.ticks_diff(now, led_timer) >= 0:
        leds_off()
        led_on = False
        led_timer = now + random.randint(300, 2000)  # Pause zwischen Blitzen

# Spiel-Logik
def spiel():
    global sequence, led_timer, runde, now, seq_index, led_on, player_index, run_game, last_press_time, senso_run
    #print(runde)
    #print("game beginn", sequence)
    #log(msg=f"{sequence}")
    if runde == 0: next_round()

     # --- SEQUENZ ABspielen ---
    if runde == 1:
        if not led_on and seq_index < len(sequence) and time.ticks_diff(now, led_timer) >= 0:
            led(sequence[seq_index])
            log(f"LED {sequence[seq_index]} an (Index {seq_index})")
            led_on = True
            led_timer = now + 700  # LED 700ms an

        elif led_on and time.ticks_diff(now, led_timer) >= 0:
            leds_off()
            log(f"LED {sequence[seq_index]} aus")
            led_on = False
            seq_index += 1
            led_timer = now + 300  # kurze Pause zwischen LEDs

        elif seq_index >= len(sequence) and not led_on:
            leds_off()
            runde = 2
            log("Sequenz fertig — Spieler dran!")

    # --- SPIELER-EINGABE ---
    elif runde == 2:
        pressed = read_button()
        if pressed > 0 and time.ticks_diff(now, last_press_time) > 400:
            last_press_time = now
            log(f"Du hast gedrückt: {pressed}")

            if pressed == sequence[player_index]:
                log("Richtig!")
                led(pressed)
                led_timer = now + 300
                player_index += 1
                while read_button() > 0:
                    log("Button pressed")
                    time.sleep(0.1)

                if player_index == len(sequence):
                    log("Runde geschafft!")
                    runde = 3          # NEUES FLAG: warte-Pause
                    led_timer = now + 800  # 0,8 Sek Pause vor der nächsten Runde
                    leds_off()
                    
                #Skill Level definition
                end_bedingungen = {
                    1: 8,
                    2: 14,
                    3: 20,
                    4: 31
                }
                if gamemode == 0:
                    if skilllevel.skill_level in end_bedingungen and player_index == end_bedingungen[skilllevel.skill_level]:
                        log("Glückwunsch: Spiel beendet")
                        senso_run = False
                        sequence.clear()
            else:  # Game Over, Variablen reset und LEDs blinken
                all_led() 
                log("Falsch! Game Over.")
                run_game = 0
                sequence.clear()
                numspieler = 0
                leds_off()
                senso_run = False
                time.sleep(1)

    # --- Warte-Pause vor der nächsten Runde ---
    elif runde == 3:
        if time.ticks_diff(now, led_timer) >= 0:
            while read_button() > 0:
                log("Button pressed")
                time.sleep(0.1)
            next_round()


def next_round():
    global player_index, seq_index, runde, led_on, led_timer, numspieler
    if gamemode in (0,3):
        sequence.append(random.randint(1, 4))
    elif gamemode == 1:
        sequence.append(random.choice(list(player_color.values())))
    elif gamemode == 2:
        if len(sequence) == 0:
            sequence.append(random.randint(1, 4))
        else:
            numspieler = numspieler + 1
            if numspieler > players:
                numspieler = 1
            menu.menutext(f"Player: {numspieler}", "center", "top", 0)
            menu.menutext("Press next", "center", "center", 0)
            menu.menutext("sequence color", "center", "bottom", 0)
            eingabe = menu.read_button(0)
            sequence.append(eingabe)
            menu.cleardisplay()
    player_index = 0
    seq_index = 0
    led_on = False
    led_timer = 0
    runde = 1
    log(f"Neue Runde! Sequenz: {sequence}")

def pre_start_senso():
    global gamemode
    menu.menu_ui.init_menu()
    menu.menutext("Set Gamemode", "title", "title", 0)
    menu.menutext("Normal Senso", "text", 1, 0)
    menu.menutext("Player Adds", "text", 2, 0)
    menu.menutext("Choose Color", "text", 3, 0)
    menu.menutext("Endless", "text", 4, 0)
    eingabe = menu.read_button(0)
    menu.cleardisplay()
    while read_button() > 0:
            log("Button pressed")
            time.sleep(0.25)
    if eingabe == 1:
        gamemode = 0
        pre_start_game_senso()
    elif eingabe == 2:
        gamemode = 2
        pre_start_playeradds()
    elif eingabe == 3:
        gamemode = 1
        pre_start_choosecolor()
    elif eingabe == 4:
        gamemode = 3
        menu.menutext("Taste druecken", "center", "top", 0)
        menu.menutext("fuer", "center", "center", 0)
        menu.menutext("Erste Sequenz", "center", "bottom", 0)
        mainloop()

def pre_start_playeradds():
    global players
    menu.menu_ui.init_menu()
    menu.menutext("Set Players", "title", "title", 0)
    menu.menutext("1 Player", "text", 1, 0)
    menu.menutext("2 Player", "text", 2, 0)
    menu.menutext("3 Player", "text", 3, 0)
    menu.menutext("4 Player", "text", 4, 0)
    eingabe = menu.read_button(0)
    players = eingabe
    menu.cleardisplay()
    mainloop()
    
def pre_start_choosecolor():
    global players, player_color
    player_color = {}
    menu.menu_ui.init_menu()
    menu.menutext("Set Players", "title", "title", 0)
    menu.menutext("1 Player", "text", 1, 0)
    menu.menutext("2 Player", "text", 2, 0)
    menu.menutext("3 Player", "text", 3, 0)
    menu.menutext("4 Player", "text", 4, 0)
    eingabe = menu.read_button(0)
    players = eingabe
    menu.cleardisplay()
    menu.menu_ui.init_menu()
    while read_button() > 0:
            log("Button pressed")
            time.sleep(0.25)
    menu.menutext("Choose Color", "title", "title", 0)
    menu.menutext("1 Player", "text", 1, 0)
    if players > 1:
        menu.menutext("2 Player", "text", 2, 0)
    if players > 2:
        menu.menutext("3 Player", "text", 3, 0)
    if players > 3:
        menu.menutext("4 Player", "text", 4, 0)
    for eingaben in range(players):
        run = True
        while run:
            while read_button() > 0:
                log("Button pressed")
                time.sleep(0.25)
            eingabe = menu.read_button(0)
            if eingabe in player_color.values():
                run = True
            else:
                player_color[eingaben + 1] = eingabe
                run = False
            
    menu.cleardisplay()
    print(player_color)
    mainloop()
    
def pre_start_game_senso():
    menu.menu_ui.init_menu()
    menu.menutext("Set Gamemode", "title", "title", 0)
    menu.menutext("Leicht", "text", 1, 0)
    menu.menutext("Mittel", "text", 2, 0)
    menu.menutext("Schwer", "text", 3, 0)
    menu.menutext("Extrem", "text", 4, 0)
    eingabe = menu.read_button(0)
    if eingabe == 1:
        skilllevel.set_skilllevel(1)
    elif eingabe == 2:
        skilllevel.set_skilllevel(2)
    elif eingabe == 3:
        skilllevel.set_skilllevel(3)
    elif eingabe == 4:
        skilllevel.set_skilllevel(4)
    menu.cleardisplay()
    while read_button() > 0:
            log("Button pressed")
            time.sleep(0.25)
    menu.menutext("Taste druecken", "center", "top", 0)
    menu.menutext("fuer", "center", "center", 0)
    menu.menutext("Erste Sequenz", "center", "bottom", 0)
    mainloop()
    
def mainloop():
    global now, run_game, st_ani, senso_run
    senso_run = True
    # Hauptloop
    while True:
        now = time.ticks_ms()
        if read_button() > 0 and run_game == 0 and senso_run == True:
            log("Game Start!")
            run_game = 1
            next_round()
        if run_game == 1:
            spiel()
        elif st_ani==True:
            start_animation()
        # LEDs ausschalten, wenn Zeit abgelaufen und keine Sequenz läuft
        if time.ticks_diff(led_timer, now) <= 0 and runde != 1:
            leds_off()
        if senso_run == False:
            run_game = 0
            sequence.clear()
            leds_off()
            time.sleep(1)
            break
    menu.cleardisplay()
    menu.menu_ui.init_menu()
    menu.menutext("Neuer Versuch", "title", "title", 0)
    menu.menutext("Nein", "text", 2, 0)
    menu.menutext("Ja", "text", 3, 0)
    eingabe = menu.read_button(0)
    menu.cleardisplay()
    if eingabe == 3:
        menu.menutext("Taste druecken", "center", "top", 0)
        menu.menutext("fuer", "center", "center", 0)
        menu.menutext("Erste Sequenz", "center", "bottom", 0)
        mainloop()
    if eingabe == 4:
        menu.menutext("zurueck Menue", "center", "center", 1)
        menu.cleardisplay()
        menu.mainmenu()
    else:
        menu.menutext("Falsche Eingabe", "center", "top", 0)
        menu.menutext("zurueck Menue", "center", "center", 1)
        menu.cleardisplay()
        menu.mainmenu()
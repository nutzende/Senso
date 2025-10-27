import time, random, pin, display as d
#TODO Taste gedrückt halten führt zu mehreren Eingaben. Variable zum Input Switch einführen
# Log Ausgabe / Start Animation / Display
dev = True
st_ani = False
display = True

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

# Debug Funktion
def log(msg):
    if dev:
        if display == True:
            global texthoehe
            if texthoehe == 0:
                d.oled.fill(0)
            if texthoehe >= 60:
                texthoehe = 0
                d.oled.fill(0)
            d.oled.text(msg, 0, texthoehe)
            d.oled.show()
            texthoehe = texthoehe + 10
        else:
            #time = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
            print(msg)

# LED Funktionen
def leds_off():
    pin.l_green.off()
    pin.l_red.off()
    pin.l_yellow.off()
    pin.l_blue.off()

def all_led():
    pin.l_green.on()
    pin.l_red.on()
    pin.l_yellow.on()
    pin.l_blue.on()

def led(num):
    leds_off()
    if num == 1: pin.l_green.on()
    elif num == 2: pin.l_red.on()
    elif num == 3: pin.l_yellow.on()
    elif num == 4: pin.l_blue.on()

# Button lesen
def read_button():
    if pin.b_green.value(): return 1
    if pin.b_red.value(): return 2
    if pin.b_yellow.value(): return 3
    if pin.b_blue.value(): return 4
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
    global sequence, led_timer, runde, now, seq_index, led_on, player_index, run_game, last_press_time
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

                if player_index == len(sequence):
                    log("Runde geschafft!")
                    runde = 3          # NEUES FLAG: warte-Pause
                    led_timer = now + 800  # 0,8 Sek Pause vor der nächsten Runde
                    leds_off()
            else:  # Game Over, Variablen reset und LEDs blinken
                all_led() 
                log("Falsch! Game Over.")
                run_game = 0
                sequence.clear()
                leds_off()
                time.sleep(1)

    # --- Warte-Pause vor der nächsten Runde ---
    elif runde == 3:
        if time.ticks_diff(now, led_timer) >= 0:
            next_round()


def next_round():
    global player_index, seq_index, runde, led_on, led_timer
    sequence.append(random.randint(1, 4))
    player_index = 0
    seq_index = 0
    led_on = False
    led_timer = 0
    runde = 1
    log(f"Neue Runde! Sequenz: {sequence}")


def mainloop():
    global now, run_game, st_ani
    # Hauptloop
    while True:
        now = time.ticks_ms()
        if read_button() > 0 and run_game == 0:
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
#mainloop()
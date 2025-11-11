import time, random, pin

def leds_off():
    l_green.off()
    l_red.off()
    l_yellow.off()
    l_blue.off()

def led(num):
    leds_off()
    if num == 1: l_green.on()
    elif num == 2: l_red.on()
    elif num == 3: l_yellow.on()
    elif num == 4: l_blue.on()

def read_button_msec(msec):
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_add(start, msec ), time.ticks_ms()) > 0 or msec == 0:
        if b_green.value(): return 1
        if b_red.value(): return 2
        if b_yellow.value(): return 3
        if b_blue.value(): return 4
    return 0

def spiel3(lvl):
    print("spiel3")
    print("Wenn sie bereit sind, beliebigen Knopf drücken")
    read_button_msec(0)
    time.sleep(0.2)
    abbr = False
    for i in range(lvl):  
        print("Runde:", i+1)  
        for j in range(4):
            mole = random.randint(1,4)
            led(mole)
            if read_button_msec(2150-(i*200)) != mole:
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
    if not abbr: print("Gewonnen!")
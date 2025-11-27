import time, neopixel, random, ssd1309, pin, display
from machine import Pin, I2C

def zeichne_text():
    """Zeichnet permanenten Text in die Mitte des Displays."""
    display.oled.text("Senso by", display.oled_width//2 - 32, display.oled_height//2 - 12)  # ungefähr mittig
    display.oled.text("Thor Tech", display.oled_width//2 - 36, display.oled_height//2 + 2)

# --------------------------
# Pixel Funktionen LEDs
# --------------------------
def set_pixel(i, r, g, b):
    pin.np[i] = (r, g, b)

def random_flash_pixel(i):
    brightness = random.randint(200, 255)
    set_pixel(i, brightness, brightness, 255)
    pin.np.write()
    time.sleep_ms(random.randint(100, 180))
    after = random.randint(80, 150)
    set_pixel(i, after, after, 255)
    pin.np.write()
    time.sleep_ms(random.randint(40, 80))
    set_pixel(i, 0, 0, 0)
    pin.np.write()

def random_flicker_pixel(i):
    intensity = random.randint(5, 120)
    set_pixel(i, intensity, intensity, 255)
    pin.np.write()
    time.sleep_ms(random.randint(20, 120))
    set_pixel(i, 0, 0, 0)
    pin.np.write()

# --------------------------
# OLED Blitze
# --------------------------
def zeichne_blitz(blitz_nr):
    """Zeichnet einen zufälligen Blitz über die volle Displayhöhe."""
    random.seed(blitz_nr)
    x = random.randint(0, display.oled_width - 1)
    y = 0
    for _ in range(25):  # Segmentanzahl
        neue_x = x + random.randint(-16, 15)
        neue_y = y + random.randint(3, 10)
        neue_x = max(0, min(display.oled_width - 1, neue_x))
        neue_y = max(0, min(display.oled_height - 1, neue_y))
        display.oled.draw_line(x, y, neue_x, neue_y)
        x, y = neue_x, neue_y
        if y >= display.oled_height - 1:
            break

# --------------------------
# Startanimation
# --------------------------
def start_animation():
    display.oled.clear_buffers()
    display.oled.show()
    # --- erster Blitzblock ---
    for blitz_nr in range(4):
        i = random.randint(0, 4 - 1)
        random_flash_pixel(i)

        display.oled.clear_buffers()
        zeichne_blitz(blitz_nr)
        zeichne_text()
        display.oled.show()
        time.sleep_ms(random.randint(40, 80))

    # --- zweiter Blitzblock ---
    for blitz_nr in range(3):
        i = random.randint(0, 4 - 1)
        random_flash_pixel(i)

        display.oled.clear_buffers()
        zeichne_blitz(blitz_nr + 10)
        zeichne_text()
        display.oled.show()
        time.sleep_ms(random.randint(40, 80))

    # --- Afterglow LEDs ---
    fades = [random.randint(150, 255) for _ in range(4)]
    for step in range(60):
        for i in range(4):
            val = max(0, fades[i] - step * 4)
            set_pixel(i, val//5, val//5, val)
        pin.np.write()
        time.sleep_ms(15)

    #Donnerflackern LEDs
    for _ in range(20):
        display.oled.clear_buffers()
        zeichne_blitz(_)
        zeichne_text()
        display.oled.show()
        for i in range(4):
            if random.random() > 0.5:
                random_flicker_pixel(i)
        time.sleep_ms(random.randint(10, 40))

    # LEDs aus
    for i in range(4):
        set_pixel(i, 0, 0, 0)
    pin.np.write()
    display.oled.clear_buffers()
    display.oled.show()
    time.sleep(0.5)
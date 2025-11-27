import time
from machine import Pin, I2C
import neopixel
import random
import ssd1309

LED_PIN = 22
LED_COUNT = 4
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

# Display initialisieren
i2c = I2C(0, scl=Pin(7), sda=Pin(8))
oled = ssd1309.Display(i2c=i2c, rst=Pin(5), width=128, height=64)

DISPLAY_BREITE = oled.width
DISPLAY_HOEHE = oled.height

def zeichne_text():
    """Zeichnet permanenten Text in die Mitte des Displays."""
    oled.text("Senso by", DISPLAY_BREITE//2 - 32, DISPLAY_HOEHE//2 - 12)  # ungefähr mittig
    oled.text("Thor Tech", DISPLAY_BREITE//2 - 36, DISPLAY_HOEHE//2 + 2)

# --------------------------
# Pixel Funktionen LEDs
# --------------------------
def set_pixel(i, r, g, b):
    np[i] = (r, g, b)

def random_flash_pixel(i):
    brightness = random.randint(200, 255)
    set_pixel(i, brightness, brightness, 255)
    np.write()
    time.sleep_ms(random.randint(100, 180))
    after = random.randint(80, 150)
    set_pixel(i, after, after, 255)
    np.write()
    time.sleep_ms(random.randint(40, 80))
    set_pixel(i, 0, 0, 0)
    np.write()

def random_flicker_pixel(i):
    intensity = random.randint(5, 120)
    set_pixel(i, intensity, intensity, 255)
    np.write()
    time.sleep_ms(random.randint(20, 120))
    set_pixel(i, 0, 0, 0)
    np.write()

# --------------------------
# OLED Blitze
# --------------------------
def zeichne_blitz(blitz_nr):
    """Zeichnet einen zufälligen Blitz über die volle Displayhöhe."""
    random.seed(blitz_nr)
    x = random.randint(0, DISPLAY_BREITE - 1)
    y = 0
    for _ in range(25):  # Segmentanzahl
        neue_x = x + random.randint(-16, 15)
        neue_y = y + random.randint(3, 10)
        neue_x = max(0, min(DISPLAY_BREITE - 1, neue_x))
        neue_y = max(0, min(DISPLAY_HOEHE - 1, neue_y))
        oled.draw_line(x, y, neue_x, neue_y)
        x, y = neue_x, neue_y
        if y >= DISPLAY_HOEHE - 1:
            break

# --------------------------
# Startanimation
# --------------------------
def start_animation():
    oled.clear_buffers()
    oled.show()

    # --- erster Blitzblock ---
    for blitz_nr in range(4):
        i = random.randint(0, LED_COUNT - 1)
        random_flash_pixel(i)

        oled.clear_buffers()
        zeichne_blitz(blitz_nr)
        zeichne_text()
        oled.show()
        time.sleep_ms(random.randint(40, 80))

    # --- zweiter Blitzblock ---
    for blitz_nr in range(3):
        i = random.randint(0, LED_COUNT - 1)
        random_flash_pixel(i)

        oled.clear_buffers()
        zeichne_blitz(blitz_nr + 10)
        zeichne_text()
        oled.show()
        time.sleep_ms(random.randint(40, 80))

    # --- Afterglow LEDs ---
    fades = [random.randint(150, 255) for _ in range(LED_COUNT)]
    for step in range(60):
        for i in range(LED_COUNT):
            val = max(0, fades[i] - step * 4)
            set_pixel(i, val//5, val//5, val)
        np.write()
        time.sleep_ms(15)

    #Donnerflackern LEDs
    for _ in range(20):
        oled.clear_buffers()
        zeichne_blitz(_)
        zeichne_text()
        oled.show()
        for i in range(LED_COUNT):
            if random.random() > 0.5:
                random_flicker_pixel(i)
        time.sleep_ms(random.randint(10, 40))

    # LEDs aus
    for i in range(LED_COUNT):
        set_pixel(i, 0, 0, 0)
    np.write()

    oled.clear_buffers()
    oled.show()
    time.sleep(0.5)
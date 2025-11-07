from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import urandom

# ====================================================
# 1. DISPLAY EINSTELLUNGEN
# ====================================================

# Breite und Höhe deines Displays
DISPLAY_BREITE = 128
DISPLAY_HOEHE = 48  # falls du ein 128x64 Display hast, ändere das zu 64

# I2C-Verbindung herstellen
# Hier werden die Pins angegeben, die mit dem Display verbunden sind
# (eventuell musst du scl/sda anpassen)
i2c = I2C(0, scl=Pin(7), sda=Pin(8))

# Display-Objekt erstellen
oled = SSD1306_I2C(DISPLAY_BREITE, DISPLAY_HOEHE, i2c)

# ====================================================
# 2. HILFSFUNKTIONEN ZUM ZEICHNEN
# ====================================================

def zeichne_linie(start_x, start_y, ende_x, ende_y):
    """
    Zeichnet eine Linie von (start_x, start_y) nach (ende_x, ende_y)
    auf dem Display mit Hilfe des Bresenham-Algorithmus.
    """
    delta_x = abs(ende_x - start_x)
    delta_y = abs(ende_y - start_y)
    schritt_x = 1 if start_x < ende_x else -1
    schritt_y = 1 if start_y < ende_y else -1
    fehler = delta_x - delta_y

    while True:
        # Pixel auf dem Display setzen
        if 0 <= start_x < DISPLAY_BREITE and 0 <= start_y < DISPLAY_HOEHE:
            oled.pixel(start_x, start_y, 1)

        # Wenn Endpunkt erreicht, abbrechen
        if start_x == ende_x and start_y == ende_y:
            break

        fehler_verdoppelt = fehler * 2

        if fehler_verdoppelt > -delta_y:
            fehler -= delta_y
            start_x += schritt_x

        if fehler_verdoppelt < delta_x:
            fehler += delta_x
            start_y += schritt_y


def schreibe_text_zentriert(text):
    """
    Schreibt den Text mittig auf das Display.
    Die Schriftgröße des SSD1306-Treibers ist 8x8 Pixel pro Zeichen.
    """
    text_breite = len(text) * 8
    start_x = (DISPLAY_BREITE - text_breite) // 2
    start_y = (DISPLAY_HOEHE // 2) - 4
    oled.text(text, start_x, start_y, 1)


# ====================================================
# 3. BLITZ-EFFEKT
# ====================================================

def zeichne_blitz(blitz_nummer):
    """
    Zeichnet mehrere zufällige Blitze, die von oben nach unten laufen.
    Jeder Blitz besteht aus mehreren schrägen Linien.
    """
    # Den Zufallsgenerator mit der Blitznummer starten,
    # damit jedes Frame anders aussieht
    urandom.seed(blitz_nummer)

    # Anzahl der Blitze pro Frame
    anzahl_blitze = 5

    for blitz_index in range(anzahl_blitze):

        # Startpunkt des Blitzes oben im Display
        aktuelle_position_x = urandom.getrandbits(7) % DISPLAY_BREITE
        aktuelle_position_y = 0

        # Jeder Blitz besteht aus mehreren Liniensegmenten
        anzahl_segmente = 15

        for segment_index in range(anzahl_segmente):

            # Der Blitz soll schräg aussehen:
            # -> größere Abweichung in x-Richtung (links/rechts)
            # -> kleinere Bewegung nach unten
            neue_position_x = aktuelle_position_x + (urandom.getrandbits(4) - 4)  # -8 bis +7
            neue_position_y = aktuelle_position_y + (urandom.getrandbits(2) + 1)  # +1 bis +4

            # Linie zwischen den beiden Punkten zeichnen
            zeichne_linie(aktuelle_position_x, aktuelle_position_y, neue_position_x, neue_position_y)

            # Aktuelle Position für das nächste Segment speichern
            aktuelle_position_x = neue_position_x
            aktuelle_position_y = neue_position_y

            # Wenn der Blitz den unteren Rand erreicht hat, abbrechen
            if aktuelle_position_y >= DISPLAY_HOEHE:
                break


# ====================================================
# 4. ANIMATION "GAME OVER"
# ====================================================

def zeige_game_over():
    """
    Zeigt mehrmals die GAME OVER-Anzeige mit Blitz-Animation.
    """
    anzahl_bilder = 10

    for frame_nummer in range(anzahl_bilder):
        # Bildschirm löschen
        oled.fill(0)

        # Text in der Mitte anzeigen
        schreibe_text_zentriert("GAME OVER")

        # Blitze für dieses Frame zeichnen
        zeichne_blitz(frame_nummer)

        # Anzeige aktualisieren
        oled.show()

        # Kurze Pause, damit man die Bewegung sieht
        time.sleep(0.2)


# ====================================================
# 5. HAUPTSCHLEIFE
# ====================================================

while True:
    # Animation einmal abspielen
    zeige_game_over()

    # Kurze Pause, bevor die Animation erneut startet
    time.sleep(2)

import display, bitmaps, menu

#Test Transparente Bitmap mit [0,1,2]
bitmap_transparent = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,2,2,2,2,2,2,0,1],
    [1,0,2,2,2,2,2,2,0,1],
    [1,0,2,2,2,2,2,2,0,1],
    [1,0,2,2,2,2,2,2,0,1],
    [1,0,2,2,2,2,2,2,0,1],
    [1,0,2,2,2,2,2,2,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]

def height(bitmap):
    height = len(bitmap)
    return height

#Für Testbitmap
width4 = len(bitmap_transparent[0])

def draw_bitmap(x, y, data, width, height, transparent):
    
    if transparent == 1:
     for row, line in enumerate(data):
        for col, val in enumerate(line):
            if val == 1:
                display.oled.draw_pixel(x + col, y + row, 0)
            elif val == 0:
                display.oled.draw_pixel(x + col, y + row, 1)
    else:
        for row in range(height):
            line = data[row]
            for col in range(width):
                # Prüfe, ob das Bit gesetzt ist (von links nach rechts)
                if (line >> (width - 1 - col)) & 1:
                    display.oled.draw_pixel(x + col, y + row, 0)
                else:
                    display.oled.draw_pixel(x + col, y + row, 1)

def init_progressbar(selectors):
    width_blitz = 11
    x_min = 13
    x_max = 106

    bar_width = x_max - x_min

    for i in range(selectors):
        x = x_min + (i * 13)
        if x <= x_max:
            y = 16
            bitmap = bitmaps.blitz
        elif x <= x_max + bar_width + 11:
            x = x - bar_width - 11
            y = 32
            bitmap = bitmaps.blitz_unfill
        else:
            x = x - 2 * bar_width - 22
            y = 48
            bitmap = bitmaps.blitz_unfill

        draw_bitmap(x, y, bitmap, width_blitz, height(bitmap), 0)

    display.oled.show()
def init_menu():
    #Hauptmenü aufbauen
    width_hcircle = 4
    width_cross = 3
    width_indicator = 8
    width_arrow = 9
    #display.graphics.line(x1, y1, x2, y2, fill)
    #linke Senkrechtlinie
    display.oled.draw_line(10, 4, 10, 59)
    #rechte Senkrechtlinie
    display.oled.draw_line(117, 4, 117, 59)
    #obere Horizontallinie
    display.oled.draw_line(5, 12, 123, 12)
    #untere Horizontallinie
    display.oled.draw_line(5, 52, 123, 52)
    #schnörkel an den Linien im Menü darstellen
    #Schnörkel oben links
    draw_bitmap(1, 9, bitmaps.hcircle_l_up, width_hcircle, height(bitmaps.hcircle_l_up), 0)
    #Schnörkel oben rechts
    draw_bitmap(123, 9, bitmaps.hcircle_r_up, width_hcircle, height(bitmaps.hcircle_r_up), 0)
    #Schnörkel oben links
    draw_bitmap(1, 52, bitmaps.hcircle_l_down, width_hcircle, height(bitmaps.hcircle_l_down), 0)
    #Schnörkel oben rechts
    draw_bitmap(123, 52, bitmaps.hcircle_r_down, width_hcircle, height(bitmaps.hcircle_r_down), 0)
    #Kreuz oben links
    draw_bitmap(9, 1, bitmaps.cross, width_cross, height(bitmaps.cross), 0)
    #Kreuz oben rechts
    draw_bitmap(116, 1, bitmaps.cross, width_cross, height(bitmaps.cross), 0)
    #Kreuz unten links
    draw_bitmap(9, 59, bitmaps.cross, width_cross, height(bitmaps.cross), 0)
    #Kreuz unten rechts
    draw_bitmap(116, 59, bitmaps.cross, width_cross, height(bitmaps.cross), 0)
    #TODO Width und Hight für Indicator zusammenfassen
    draw_bitmap(1, 16, bitmaps.indicator_button_blue, width_indicator, height(bitmaps.indicator_button_blue), 0)
    draw_bitmap(1, 25, bitmaps.indicator_button_red, width_indicator, height(bitmaps.indicator_button_red), 0)
    draw_bitmap(1, 34, bitmaps.indicator_button_green, width_indicator, height(bitmaps.indicator_button_green), 0)
    draw_bitmap(1, 43, bitmaps.indicator_button_yellow, width_indicator, height(bitmaps.indicator_button_yellow), 0)
    #draw_bitmap(119, 16, bitmaps.arrow, width_arrow, height(bitmaps.arrow), 0)
    # Anzeigen
    display.oled.show()
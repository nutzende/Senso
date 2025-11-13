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

def width(bitmap):
    width = max(line.bit_length() for line in bitmap)
    return width

#Für Testbitmap
width4 = len(bitmap_transparent[0])

def draw_bitmap(x, y, data, width, height, transparent):
    
    if transparent == 1:
     for row, line in enumerate(data):
        for col, val in enumerate(line):
            if val == 1:
                display.oled.pixel(x + col, y + row, 1)
            elif val == 0:
                display.oled.pixel(x + col, y + row, 0)
    else:
        for row in range(height):
            line = data[row]
            for col in range(width):
                # Prüfe, ob das Bit gesetzt ist (von links nach rechts)
                if (line >> (width - 1 - col)) & 1:
                    display.oled.pixel(x + col, y + row, 1)
                else:
                    display.oled.pixel(x + col, y + row, 0)
                    
def init_menu():
    #Hauptmenü aufbauen
    #display.graphics.line(x1, y1, x2, y2, fill)
    #linke Senkrechtlinie
    display.graphics.line(10, 4, 10, 59, 1)
    #rechte Senkrechtlinie
    display.graphics.line(116, 4, 116, 59, 1)
    #obere Horizontallinie
    display.graphics.line(5, 13, 123, 13, 1)
    #untere Horizontallinie
    display.graphics.line(5, 53, 123, 53, 1)
    #draw_bitmap(0, 0, bitmaps.menu_ui, width(bitmaps.menu_ui), height(bitmaps.menu_ui), 0)
    
    width_hcircle = 4
    width_cross = 3
    width_indicator = 8
    #schnörkel an den Linien im Menü darstellen
    #Schnörkel oben links
    draw_bitmap(1, 10, bitmaps.hcircle_l_up, width_hcircle, height(bitmaps.hcircle_l_up), 0)
    #Schnörkel oben rechts
    draw_bitmap(124, 10, bitmaps.hcircle_r_up, width_hcircle, height(bitmaps.hcircle_r_up), 0)
    #Schnörkel oben links
    draw_bitmap(1, 53, bitmaps.hcircle_l_down, width_hcircle, height(bitmaps.hcircle_l_down), 0)
    #Schnörkel oben rechts
    draw_bitmap(124, 53, bitmaps.hcircle_r_down, width_hcircle, height(bitmaps.hcircle_r_down), 0)

    
    #Kreuz oben links
    draw_bitmap(9, 1, bitmaps.cross, width_cross, height(bitmaps.cross), 0)
    #Kreuz oben rechts
    draw_bitmap(115, 1, bitmaps.cross, width_cross, height(bitmaps.cross), 0)
    #Kreuz unten links
    draw_bitmap(9, 59, bitmaps.cross, width_cross, height(bitmaps.cross), 0)
    #Kreuz unten rechts
    draw_bitmap(115, 59, bitmaps.cross, width_cross, height(bitmaps.cross), 0)
    #TODO Width und Hight für Indicator zusammenfassen
    draw_bitmap(1, 16, bitmaps.indicator_button_blue, width_indicator, height(bitmaps.indicator_button_blue), 0)
    draw_bitmap(1, 25, bitmaps.indicator_button_red, width_indicator, height(bitmaps.indicator_button_red), 0)
    draw_bitmap(1, 34, bitmaps.indicator_button_green, width_indicator, height(bitmaps.indicator_button_green), 0)
    draw_bitmap(1, 43, bitmaps.indicator_button_yellow, width_indicator, height(bitmaps.indicator_button_yellow), 0)

    #Test Texte Anzeigen
    #menu.menutext(TEXT, X-Pos, Y Line, SEC)
    menu.menutext("Senso", "text", 1, 0)
    menu.menutext("Bottle spin", "text", 2, 0)
    menu.menutext("test3", "text", 3, 0)
    menu.menutext("test4", "text", 4, 0)
    # Anzeigen
    display.oled.show()
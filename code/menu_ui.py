import display, bitmaps

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
    """Zeichnet eine monochrome Bitmap auf das OLED."""
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
    draw_bitmap(0, 0, bitmaps.menu_ui, width(bitmaps.menu_ui), height(bitmaps.menu_ui), 0)
    draw_bitmap(1, 16, bitmaps.indicator_button_blue, width(bitmaps.indicator_button_blue), height(bitmaps.indicator_button_blue), 0)
    draw_bitmap(1, 25, bitmaps.indicator_button_red, width(bitmaps.indicator_button_red), height(bitmaps.indicator_button_red), 0)
    draw_bitmap(1, 34, bitmaps.indicator_button_green, width(bitmaps.indicator_button_green), height(bitmaps.indicator_button_green), 0)
    draw_bitmap(1, 43, bitmaps.indicator_button_yellow, width(bitmaps.indicator_button_yellow), height(bitmaps.indicator_button_yellow), 0)
    draw_bitmap(20, 0, bitmap_transparent, width4, height(bitmap_transparent), 1)
    #Test Texte Anzeigen
    display.oled.text("Senso", "text", 1)
    display.oled.text("Bottle spin", "text", 2)
    display.oled.text("test3", "text", 3)
    display.oled.text("test4", "text", 4)
    # Anzeigen
    display.oled.show()
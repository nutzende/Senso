import machine, neopixel

n = 4
p = 15

np = neopixel.NeoPixel(machine.Pin(p), n)

np[0] = (0,0,255)
np[1] = (255,255,0)
np[2] = (255,0,0)
np[3] = (0,255,0)
np.write()
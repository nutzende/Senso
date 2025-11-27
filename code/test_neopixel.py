import machine, neopixel

n = 4
p = 22

np = neopixel.NeoPixel(machine.Pin(p), n)

np[2] = (0,0,255)
np[3] = (255,255,0)
np[0] = (0,255,0)
np[1] = (255,0,0)

np.write()
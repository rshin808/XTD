# Libraries
import seps525
from text import Text_string as TS
import RPi.GPIO as gpio
import csv
from font import Font
import spidev
import time

# Initialize Fonts
font14h = Font("font14h")
font14h.init_bitmap("font14h.csv")
font14hL = Font("font14hL.csv")
font14hL.init_bitmap("font14hL.csv")

# Initialize Display
display = seps525.SEPS525_nhd()
display.fill_screen((255,255))

# Set GPIO
gpio.setmode(gpio.BCM)

# Set Label Strings
bma = "BMA:"
bmb = "BMB:"
testCircuit = "TEST CIRCUIT:"
pll = "PLL:"
schrod = "SCHROD:"

# Set Label Values
bmaValue = "0"
bmbValue = "100"
testCircuitValue = "ON"
pllValue = "LOCKED"
schrodValue = "A"

try:
    # Draw Labels
    loffset = 10
    bmaDisp = TS(loffset, 10, 14, bma, font14h)
    bmbDisp = TS(loffset, 26, 14, bmb, font14h)
    testCircuitDisp = TS(loffset, 42, 14, testCircuit, font14h)
    pllDisp = TS(loffset, 58, 14, pll, font14h)
    schrodDisp = TS(loffset, 74, 14, schrod, font14h)

    bmaDisp.draw_string((0, 0), (255, 255), display)
    bmbDisp.draw_string((0, 0), (255, 255), display)
    testCircuitDisp.draw_string((0, 0), (255, 255), display)
    pllDisp.draw_string((0, 0), (255, 255), display)
    schrodDisp.draw_string((0, 0), (255, 255), display)

    # Draw Values
    loffset = 20
    bmaValueDisp = TS(loffset + len(bmaDisp), 10, 14, bmaValue, font14h)
    bmbValueDisp = TS(loffset + len(bmbDisp), 26, 14, bmbValue, font14h)
    testCircuitValueDisp = TS(loffset + len(testCircuitDisp), 42, 14, testCircuitValue, font14h)
    pllValueDisp = TS(loffset + len(pllDisp), 58, 14, pllValue, font14h)
    schrodValueDisp = TS(loffset + len(schrodDisp), 74, 14, schrodValue, font14h)

    bmaValueDisp.draw_string((0, 0), (255, 255), display)
    bmbValueDisp.draw_string((0, 0), (255, 255), display)
    testCircuitValueDisp.draw_string((0, 0), (255, 255), display)
    pllValueDisp.draw_string((0, 0), (255, 255), display)
    schrodValueDisp.draw_string((0, 0), (255, 255), display)
        

    while(True):
        pass
except KeyboardInterrupt:
    gpio.cleanup()

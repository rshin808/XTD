from userSettings import *
import RPi.GPIO as GPIO
from smbus import SMBus
from si5338POST import *
from REGS import *
from PINS import *
from bunchMarker import *
import time
import seps525
from text import Text_string as TS
import csv
from font import Font
import spidev
from getIP import *
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS["TESTEN"], GPIO.OUT)
GPIO.setup(PINS["JTAGSEL"], GPIO.OUT)

GPIO.output(PINS["TESTEN"], True)


bus = SMBus(1)

user = userSettings()
print "PLL Select: (0: RF or 1: VCO)"
vco = raw_input()

user.vco = bool(int(vco))

print bcolors.WARNING + "Loading PLL" + bcolors.ENDC
pll = si5338POST(0x70, user.vco, bus, VCOREGS, PINS["INTERRUPT"], GPIO)
time.sleep(0.5)
if pll.check():
    print bcolors.FAIL + "Exiting..." + bcolors.ENDC
    exit()
else:
    print bcolors.OKGREEN + "PLL Ready" + bcolors.ENDC


bus.close()

print "Enable Test Signal: (0: Disable or 1: Enable)"
testSignal = raw_input()
print "\n" + "Select JTAG: (0: A&B or 1: A)"
jtag = raw_input()
print "\n"+"Input bunchMarkerA: (0 - 5280)"
bma = raw_input()
print "\n"+"Input bunchMarkerB: (0 - 5280)"
bmb = raw_input()

print bin(int(bma))
print bin(int(bmb))

user.testSignal = bool(int(testSignal))
user.jtag = bool(int(jtag))


if bool(user.testSignal) == True:
    print bcolors.OKGREEN + "Test Signal ON" + bcolors.ENDC
    GPIO.output(PINS["TESTEN"], True)
else:
    GPIO.output(PINS["TESTEN"], False)

if user.scrod == True:
    print bcolors.OKGREEN + "JTAG A SELECTED" + bcolors.ENDC
    GPIO.output(PINS["JTAGSEL"], True)
else:
    print bcolors.OKGREEN + "JTAG A&B SELECTED" + bcolors.ENDC
    GPIO.output(PINS["JTAGSEL"], False)

user.bunchMarkerA = int(bma)
user.bunchMarkerB = int(bmb)

BMA = bunchMarker(PINS["BMASRCLK"], PINS["BMARCLK"], PINS["SRA"], GPIO)
BMB = bunchMarker(PINS["BMBSRCLK"], PINS["BMBRCLK"], PINS["SRB"], GPIO)

BMA.reset()
BMB.reset()

BMA.bunchMarker(user.bunchMarkerA)
BMB.bunchMarker(user.bunchMarkerB)

show = True
print "SHOW DISPLAY: (0: No or 1: Yes)"
show = bool(int(raw_input()))


# Initialize Fonts
font14h = Font("font14h")
font14h.init_bitmap("font14h.csv")
font14hL = Font("font14hL.csv")
font14hL.init_bitmap("font14hL.csv")

# Initialize Display

# Set Label Strings
inputTitle = "XTD:"
bmaTitle = "BMA:"
bmbTitle = "BMB:"
testCircuitTitle = "TEST CIRCUIT:"
pllTitle = "PLL:"
jtagTitle = "JTAG:"
IPTitle = "IP:"
IPValue = getIP()

# Set Label Values
bmaValue = str(user.bunchMarkerA)
bmbValue = str(user.bunchMarkerB)
testCircuitValue = " "
if user.testSignal == True:
    testCircuitValue = "ON"
else:
    testCircuitValue = "OFF"
pllValue = "LOCKED"
if user.jtag == True:
    jtagValue = "A"
else:
    jtagValue = "AB"

try:
    while(True):
        if show:
            display = seps525.SEPS525_nhd(DC = PINS["DISPDC"], RES = PINS["DISPRES"], gpio = GPIO)
            display.fill_screen((255,255))
            
            # Draw Labels
            loffset = 10
            bmaDisp = TS(loffset, 10, 14, bmaTitle, font14h)
            bmbDisp = TS(loffset, 26, 14, bmbTitle, font14h)
            testCircuitDisp = TS(loffset, 42, 14, testCircuitTitle, font14h)
            pllDisp = TS(loffset, 58, 14, pllTitle, font14h)
            jtagDisp = TS(loffset, 74, 14, jtagTitle, font14h)
            IPDisp = TS(loffset, 106, 14, IPTitle, font14h)

            bmaDisp.draw_string((0, 0), (255, 255), display)
            bmbDisp.draw_string((0, 0), (255, 255), display)
            testCircuitDisp.draw_string((0, 0), (255, 255), display)
            pllDisp.draw_string((0, 0), (255, 255), display)
            jtagDisp.draw_string((0, 0), (255, 255), display)
            IPDisp.draw_string((0, 0), (255, 255), display)

            # Draw Values
            loffset = 20
            bmaValueDisp = TS(loffset + len(bmaDisp), 10, 14, bmaValue, font14h)
            bmbValueDisp = TS(loffset + len(bmbDisp), 26, 14, bmbValue, font14h)
            testCircuitValueDisp = TS(loffset + len(testCircuitDisp), 42, 14, testCircuitValue, font14h)
            pllValueDisp = TS(loffset + len(pllDisp), 58, 14, pllValue, font14h)
            jtagValueDisp = TS(loffset + len(jtagDisp), 74, 14, jtagValue, font14h)
            IPValueDisp = TS(loffset + len(IPDisp), 106, 14, IPValue, font14h)

            bmaValueDisp.draw_string((0, 0), (255, 255), display)
            bmbValueDisp.draw_string((0, 0), (255, 255), display)
            testCircuitValueDisp.draw_string((0, 0), (255, 255), display)
            pllValueDisp.draw_string((0, 0), (255, 255), display)
            jtagValueDisp.draw_string((0, 0), (255, 255), display)
            IPValueDisp.draw_string((0, 0), (255, 255), display)

            IPValue = getIP()
        
        print "Enable Test Signal: (0: Disable or 1: Enable)"
        testSignal = raw_input()
        print "\n" + "Select JTAG: (0: A&B or 1: A)"
        jtag = raw_input()

        print "\n"+"Select JTAG: (0: A&B or 1: A)"
        jtag = raw_input()

        user.testSignal = bool(int(testSignal))
        user.jtag = bool(int(jtag))

        if user.jtag == True:
            print bcolors.OKGREEN + "JTAG A SELECTED" + bcolors.ENDC
            GPIO.output(PINS["JTAGSEL"], True)
        else:
            print bcolors.OKGREEN + "JTAG A&B SELECTED" + bcolors.ENDC
            GPIO.output(PINS["JTAGSEL"], False)
       
        if user.jtag == True:
            jtagValue = "A"
        else:
            jtagValue = "AB"

        print "Input new bunchMarkerA: (0 - 5280)"
        bma = raw_input()
        print "Input new bunchMarkerB: (0 - 5280)"
        bmb = raw_input()

        user.bunchMarkerA = int(bma)
        user.bunchMarkerB = int(bmb)

        BMA = bunchMarker(PINS["BMASRCLK"], PINS["BMARCLK"], PINS["SRA"], GPIO)
        BMB = bunchMarker(PINS["BMBSRCLK"], PINS["BMBRCLK"], PINS["SRB"], GPIO)

        BMA.reset()
        BMB.reset()

        BMA.bunchMarker(user.bunchMarkerA)
        BMB.bunchMarker(user.bunchMarkerB)
        bmaValue = str(user.bunchMarkerA)
        bmbValue = str(user.bunchMarkerB)
        

except KeyboardInterrupt:
    pass

GPIO.cleanup()

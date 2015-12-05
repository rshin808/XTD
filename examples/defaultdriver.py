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

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS["TESTEN"], GPIO.OUT)
GPIO.setup(PINS["SCRODSEL"], GPIO.OUT)

GPIO.output(PINS["TESTEN"], True)


bus = SMBus(1)
#user interactive components are commented out for default driver
user = userSettings()
vco = 0

user.vco = bool(int(vco))
print bcolors.WARNING + "Loading PLL" + bcolors.ENDC
pll = si5338POST(0x70, user.vco, bus, VCOREGS, PINS["INTERRUPT"], GPIO)
time.sleep(30)
try:
    if pll.check():
        print bcolors.FAIL + "Exiting..." + bcolors.ENDC
    else:
        print bcolors.OKGREEN + "PLL Ready" + bcolors.ENDC
except Exception, e:
    import csv
    with open("log.txt", "a") as logFile:
        csvW = csv.writer(logFile)
        row = [str(e)]
        csvW.writerow(row)
    time.sleep(30)
    if pll.check():
        pass
    else:
        pass

vco = 1

bus.close()
'''
print "Enable Test Signal: (0: Disable or 1: Enable)"
testSignal = raw_input()
print "Select SCROD: (A or A&B)"i
scrod = raw_input()
print "Input bunchMarkerA: (0 - 5280)"
bma = raw_input()
print "Input bunchMarkerB: (0 - 5280)"
bmb = raw_input()

print bin(int(bma))
print bin(int(bmb))
'''
testSignal = 0
scrod = 1
bma = 1000
bmb = 1500 

user.testSignal = bool(int(testSignal))
user.scrod = bool(int(scrod))


if bool(user.testSignal) == True:
    print bcolors.OKGREEN + "Test Signal ON" + bcolors.ENDC
    GPIO.output(PINS["TESTEN"], True)

if user.scrod == True:
    print bcolors.OKGREEN + "SCROD A SELECTED" + bcolors.ENDC
    GPIO.output(PINS["SCRODSEL"], True)
else:
    print bcolors.OKGREEN + "SCROD A&B SELECTED" + bcolors.ENDC
    GPIO.output(PINS["SCRODSEL"], False)

user.bunchMarkerA = int(bma)
user.bunchMarkerB = int(bmb)

BMA = bunchMarker(PINS["BMASRCLK"], PINS["BMARCLK"], PINS["SRA"], GPIO)
BMB = bunchMarker(PINS["BMBSRCLK"], PINS["BMBRCLK"], PINS["SRB"], GPIO)

BMA.reset()
BMB.reset()

BMA.bunchMarker(user.bunchMarkerA)
BMB.bunchMarker(user.bunchMarkerB)


# Initialize Fonts
font14h = Font("font14h")
font14h.init_bitmap("font14h.csv")
font14hL = Font("font14hL.csv")
font14hL.init_bitmap("font14hL.csv")

# Initialize Display

# Set Label Strings
bmaTitle = "BMA:"
bmbTitle = "BMB:"
testCircuit = "TEST CIRCUIT:"
pllTitle = "PLL:"
schrod = "SCROD:"
IPTitle = "IP:"
IPValue = getIP()


# Set Label Values
bmaValue = str(user.bunchMarkerA)
bmbValue = str(user.bunchMarkerB)
testCircuitValue = ""
if user.testSignal == True:
    testCircuitValue = "ON"
else:
    testCircuitValue = "OFF"
pllValue = "LOCKED"
schrodValue = ""
if user.scrod == True:
    schrodValue = "A"
else:
    schrodValue = "AB"

try:
    display = seps525.SEPS525_nhd(DC = PINS["DISPDC"], RES = PINS["DISPRES"], gpio = GPIO)
    display.fill_screen((255,255))
    while(True):          
        # Draw Labels
        loffset = 10
        bmaDisp = TS(loffset, 10, 14, bmaTitle, font14h)
        bmbDisp = TS(loffset, 26, 14, bmbTitle, font14h)
        testCircuitDisp = TS(loffset, 42, 14, testCircuit, font14h)
        pllDisp = TS(loffset, 58, 14, pllTitle, font14h)
        schrodDisp = TS(loffset, 74, 14, schrod, font14h)
        IPDisp = TS(loffset, 90, 14, IPTitle, font14h)

        bmaDisp.draw_string((0, 0), (255, 255), display)
        bmbDisp.draw_string((0, 0), (255, 255), display)
        testCircuitDisp.draw_string((0, 0), (255, 255), display)
        pllDisp.draw_string((0, 0), (255, 255), display)
        schrodDisp.draw_string((0, 0), (255, 255), display)
        IPDisp.draw_string((0, 0), (255, 255), display)

        # Draw Values
        loffset = 20
        bmaValueDisp = TS(loffset + len(bmaDisp), 10, 14, bmaValue, font14h)
        bmbValueDisp = TS(loffset + len(bmbDisp), 26, 14, bmbValue, font14h)
        testCircuitValueDisp = TS(loffset + len(testCircuitDisp), 42, 14, testCircuitValue, font14h)
        pllValueDisp = TS(loffset + len(pllDisp), 58, 14, pllValue, font14h)
        schrodValueDisp = TS(loffset + len(schrodDisp), 74, 14, schrodValue, font14h)
        IPValueDisp = TS(loffset + len(IPDisp), 90, 14, IPValue, font14h)        

        bmaValueDisp.draw_string((0, 0), (255, 255), display)
        bmbValueDisp.draw_string((0, 0), (255, 255), display)
        testCircuitValueDisp.draw_string((0, 0), (255, 255), display)
        pllValueDisp.draw_string((0, 0), (255, 255), display)
        schrodValueDisp.draw_string((0, 0), (255, 255), display)
        IPValueDisp.draw_string((0, 0), (255, 255), display)
        
        if pll.check():
            pllValue="WARNING"
        else:
            pllValue="LOCKED"
        

except Exception, e:
    import csv
    with open("log.txt", "a") as logFile:
        csvW = csv.writer(logFile)
        row = [str(e)]
        csvW.writerow(row)

GPIO.cleanup()

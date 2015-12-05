from userSettings import *
from smbus import SMBus
from si5338POST import *
from REGS import *
from PINS import *
import RPi.GPIO as GPIO
from bunchMarker import *

GPIO.setmode(GPIO.BCM)

bus = SMBus(1)

user = userSettings()
print "VCO: (0 or 1)"
vco = raw_input()

user.vco = bool(int(vco))

print "Loading PLL"
pll = si5338POST(0x70, user.vco, bus, VCOREGS, PINS["INTERRUPT"], GPIO)

if pll.check():
    print "Exiting..."
    exit()
else:
    print "PLL Ready"

bus.close()

print "Test Signal: (0 or 1)"
testSignal = raw_input()
print "SCROD: (A or B)"
scrod = raw_input()
print "bunchMarkerA: (0 - 5280)"
bma = raw_input()
print "bunchMarkerB: (0 - 5280)"
bmb = raw_input()

user.testSignal = bool(int(testSignal))
user.scrod = scrod

if user.testSignal == True:
    GPIO.output(PINS["TESTEN"], True)

if user.scrod == "a":
    GPIO.output(PINS["SCRODSEL"], True)
else:
    GPIO.output(PINS["SCRODSEL"], False)

user.bunchMarkerA = int(bma)
user.bunchMarkerB = int(bmb)


BMA = bunchMarker(PINS["BMASRCLK"], PINS["BMARCLK"], PINS["SRA"], GPIO)
BMB = bunchMarker(PINS["BMBSRCLK"], PINS["BMBRCLK"], PINS["SRB"], GPIO)

BMA.reset()
BMB.reset()

BMA.bunchMarker(user.bunchMarkerA)
BMB.bunchMarker(user.bunchMarkerB)

GPIO.cleanup()

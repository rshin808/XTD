#!/usr/bin/env python

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
import shutdown

# Default Values
osc = 1
testSignal = 0
jtag = 1
bma = 501 
bmb = 499 



#GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS["TESTEN"], GPIO.OUT)
GPIO.setup(PINS["SCRODSEL"], GPIO.OUT)
GPIO.setup(PINS["TEST1"], GPIO.IN)
GPIO.output(PINS["TESTEN"], True)


bus = SMBus(1)
#user interactive components are commented out for default driver
user = userSettings()

user.osc = bool(int(osc))
print bcolors.WARNING + "Loading PLL" + bcolors.ENDC
pll = si5338POST(0x70, user.osc, bus, VCOREGS, PINS["INTERRUPT"], GPIO)
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

user.testSignal = bool(int(testSignal))
user.jtag = bool(int(jtag))


if bool(user.testSignal) == True:
    print bcolors.OKGREEN + "Test Signal ON" + bcolors.ENDC
    GPIO.output(PINS["TESTEN"], True)

if user.jtag == True:
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
inputTitle = "XTD:"
bmaTitle = "BMA:"
bmbTitle = "BMB:"
testCircuit = "TEST CIRCUIT:"
pllTitle = "PLL:"
jtagTitle = "JTAG:"
IPTitle = "IP:"
IPValue = getIP()


# Set Label Values
inputValue = ""
if user.osc == 0:
    inputValue = "RF"
else:
    inputValue = "OSC"
bmaValue = str(user.bunchMarkerA)
bmbValue = str(user.bunchMarkerB)
testCircuitValue = ""
if user.testSignal == True:
    testCircuitValue = "ON"
else:
    testCircuitValue = "OFF"
pllValue = "LOCKED"
jtagValue = ""
if user.jtag == True:
    jtagValue = "A"
else:
    jtagValue = "AB"

try:
    display = seps525.SEPS525_nhd(DC = PINS["DISPDC"], RES = PINS["DISPRES"], gpio = GPIO)
    display.fill_screen((255,255))
    count = 50
    while(True):          
        BMB.bunchMarker(int(user.bunchMarkerB) + count)
        time.sleep(0.2)
        bmbValue = str(int(user.bunchMarkerB) + count)
        # Draw Labels
        loffset = 10
        inputDisp = TS(loffset, 10, 14, inputTitle, font14h)
        bmaDisp = TS(loffset, 26, 14, bmaTitle, font14h)
        bmbDisp = TS(loffset, 42, 14, bmbTitle, font14h)
        testCircuitDisp = TS(loffset, 58, 14, testCircuit, font14h)
        pllDisp = TS(loffset, 74, 14, pllTitle, font14h)
        jtagDisp = TS(loffset, 90, 14, jtagTitle, font14h)
        IPDisp = TS(loffset, 106, 14, IPTitle, font14h)

        inputDisp.draw_string((0, 0), (255, 255), display)
        bmaDisp.draw_string((0, 0), (255, 255), display)
        bmbDisp.draw_string((0, 0), (255, 255), display)
        testCircuitDisp.draw_string((0, 0), (255, 255), display)
        pllDisp.draw_string((0, 0), (255, 255), display)
        jtagDisp.draw_string((0, 0), (255, 255), display)
        IPDisp.draw_string((0, 0), (255, 255), display)

        # Draw Values
        loffset = 20
        inputValueDisp = TS(loffset + len(inputDisp), 10, 14, inputValue, font14h)
        bmaValueDisp = TS(loffset + len(bmaDisp), 26, 14, bmaValue, font14h)
        bmbValueDisp = TS(loffset + len(bmbDisp), 42, 14, bmbValue, font14h)
        testCircuitValueDisp = TS(loffset + len(testCircuitDisp), 58, 14, testCircuitValue, font14h)
        pllValueDisp = TS(loffset + len(pllDisp), 74, 14, pllValue, font14h)
        jtagValueDisp = TS(loffset + len(jtagDisp), 90, 14, jtagValue, font14h)
        IPValueDisp = TS(loffset + len(IPDisp), 106, 14, IPValue, font14h)        

        inputValueDisp.draw_string((0, 0), (255, 255), display)
        bmaValueDisp.draw_string((0, 0), (255, 255), display)
        bmbValueDisp.draw_string((0, 0), (255, 255), display)
        testCircuitValueDisp.draw_string((0, 0), (255, 255), display)
        pllValueDisp.draw_string((0, 0), (255, 255), display)
        jtagValueDisp.draw_string((0, 0), (255, 255), display)
        IPValueDisp.draw_string((0, 0), (255, 255), display)
        
        IPValue = getIP()

        if pll.check():
            pllValue="WARNING"
        else:
            pllValue="LOCKED"
        
        count += 50
except Exception, e:
    import csv
    with open("log.txt", "a") as logFile:
        csvW = csv.writer(logFile)
        row = [str(e)]
        csvW.writerow(row)

GPIO.cleanup()


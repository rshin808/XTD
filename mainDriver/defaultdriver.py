#!/usr/bin/env python

from userSettings import *
import RPi.GPIO as GPIO
from smbus import SMBus
from si5338POST import *
from REGS import *
from PINS import *
import time
import seps525
from text import Text_string as TS
import csv
from font import Font
import spidev
from getIP import *
import os

# Default Values
osc        = 0   # 0 = RFin; 1 = osc
testSignal = 1   # 0 = off; 1 = on
jtag       = 1   # 1 = SCROD A; 0 = SCROD A+B
bma        = 0000 # 5,4 pair
bmb        = 0000 # 1,2 pair

foreground = (255,0)
background = (0,0)
server_mode = 0

#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS["TESTEN"], GPIO.OUT)
GPIO.setup(PINS["JTAGSEL"], GPIO.OUT)
GPIO.setup(PINS["SHUTDOWN"], GPIO.IN)
GPIO.output(PINS["TESTEN"], True)

user = userSettings()

from bunchMarker import *
user.bunchMarkerA = int(bma)
user.bunchMarkerB = int(bmb)
BMA = bunchMarker(PINS["BMASRCLK"], PINS["BMARCLK"], PINS["SRA"], GPIO)
BMB = bunchMarker(PINS["BMBSRCLK"], PINS["BMBRCLK"], PINS["SRB"], GPIO)
BMA.reset()
BMB.reset()
BMA.bunchMarker(user.bunchMarkerA)
BMB.bunchMarker(user.bunchMarkerB)

bus = SMBus(1)
#user interactive components are commented out for default driver

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

user.testSignal = bool(int(testSignal))
user.jtag = bool(int(jtag))

if bool(user.testSignal) == True:
    print bcolors.OKGREEN + "Test Signal ON" + bcolors.ENDC
    GPIO.output(PINS["TESTEN"], True)
else:
    print bcolors.OKGREEN + "Test Signal OFF" + bcolors.ENDC
    GPIO.output(PINS["TESTEN"], False)

if user.jtag == True:
    print bcolors.OKGREEN + "JTAG A SELECTED" + bcolors.ENDC
    GPIO.output(PINS["JTAGSEL"], True)
else:
    print bcolors.OKGREEN + "JTAG A&B SELECTED" + bcolors.ENDC
    GPIO.output(PINS["JTAGSEL"], False)

# Initialize Fonts
font14h = Font("font14h")
font14h.init_bitmap("font14h.csv")
font14hL = Font("font14hL.csv")
font14hL.init_bitmap("font14hL.csv")

# Initialize Display

# Set Label Strings
inputTitle  = " XTD:"
bmaTitle    = " BMA:"
bmbTitle    = " BMB:"
testCircuit = "OUTS:"
pllTitle    = " PLL:"
jtagTitle   = "JTAG:"
IPTitle     = "  IP:"
IPValue     = getIP()

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

display = seps525.SEPS525_nhd(DC = PINS["DISPDC"], RES = PINS["DISPRES"], gpio = GPIO)

loffset = 10
inputDisp = TS(loffset, 10, 14, inputTitle, font14h)
bmaDisp = TS(loffset, 26, 14, bmaTitle, font14h)
bmbDisp = TS(loffset, 42, 14, bmbTitle, font14h)
testCircuitDisp = TS(loffset, 58, 14, testCircuit, font14h)
pllDisp = TS(loffset, 74, 14, pllTitle, font14h)
jtagDisp = TS(loffset, 90, 14, jtagTitle, font14h)
IPDisp = TS(loffset, 106, 14, IPTitle, font14h)

def draw_labels():
    display.fill_screen(background)
    # Draw Labels
    inputDisp.draw_string(foreground, background, display)
    bmaDisp.draw_string(foreground, background, display)
    bmbDisp.draw_string(foreground, background, display)
    testCircuitDisp.draw_string(foreground, background, display)
    pllDisp.draw_string(foreground, background, display)
    jtagDisp.draw_string(foreground, background, display)
    IPDisp.draw_string(foreground, background, display)

def update_display():
    if pll.check():
        pllValue="NOT LOCKED!"
    else:
        pllValue="LOCKED       "
    IPValue = getIP()
    # Draw Values
    loffset = 20
    inputValueDisp = TS(loffset + len(inputDisp), 10, 14, inputValue, font14h)
    bmaValueDisp = TS(loffset + len(bmaDisp), 26, 14, bmaValue, font14h)
    bmbValueDisp = TS(loffset + len(bmbDisp), 42, 14, bmbValue, font14h)
    testCircuitValueDisp = TS(loffset + len(testCircuitDisp), 58, 14, testCircuitValue, font14h)
    pllValueDisp = TS(loffset + len(pllDisp), 74, 14, pllValue, font14h)
    jtagValueDisp = TS(loffset + len(jtagDisp), 90, 14, jtagValue, font14h)
    IPValueDisp = TS(loffset + len(IPDisp), 106, 14, IPValue, font14h)
    inputValueDisp.draw_string(foreground, background, display)
    bmaValueDisp.draw_string(foreground, background, display)
    bmbValueDisp.draw_string(foreground, background, display)
    testCircuitValueDisp.draw_string(foreground, background, display)
    pllValueDisp.draw_string(foreground, background, display)
    jtagValueDisp.draw_string(foreground, background, display)
    IPValueDisp.draw_string(foreground, background, display)

def shutdown():
    loffset = 10
    display.fill_screen(background)
    shutdownDisp = TS(loffset, 26, 14, "Shutting Down", font14h)
    descDisp1 = TS(loffset, 42, 14, "Wait for Screen", font14h)
    descDisp2 = TS(loffset, 74, 14, "to Disappear", font14h)
    shutdownDisp.draw_string(foreground, background, display)
    descDisp1.draw_string(foreground, background, display)
    descDisp2.draw_string(foreground, background, display)
    os.system("shutdown -h now")

try:
    draw_labels()
    update_display()
    while server_mode:
        update_display()
        if GPIO.input(PINS["SHUTDOWN"]) == False: # depends on polarity of shutdown button
            shutdown()
            break;
except Exception, e:
    import csv
    with open("log.txt", "a") as logFile:
        csvW = csv.writer(logFile)
        row = [str(e)]
        csvW.writerow(row)


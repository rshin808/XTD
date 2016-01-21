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
GPIO.setup(PINS["SHUTDOWN"], GPIO.IN)
GPIO.output(PINS["TESTEN"], False)
show = True
bus = SMBus(1)
user = userSettings()

#asking user for inputs 
print "PLL Select: (0: RF or 1: VCO)"
osc = raw_input()
print "\n"+"Enable Test Signal: (0: Disable or 1: Enable)"
testSignal = raw_input()
print "\n" + "Select JTAG: (0: A&B or 1: A)"
jtag = raw_input()
print "\n"+"Input bunchMarkerA: (0 - 5280)"
bma = raw_input()
print "\n"+"Input bunchMarkerB: (0 - 5280)"
bmb = raw_input()
#print "\n"+"SHOW DISPLAY: (0: No or 1: Yes)"
#show = bool(int(raw_input()))

user.osc = bool(int(osc))
user.testSignal = bool(int(testSignal))
user.jtag = bool(int(jtag))
user.bunchMarkerA = int(bma)
user.bunchMarkerB = int(bmb)

#configuring XTD
if bool(user.testSignal) == True:
    print bcolors.OKGREEN + "Test Signal ON" + bcolors.ENDC
    GPIO.output(PINS["TESTEN"], True)
else:
    print bcolors.OKGREEN + "Test Signal OFF" + bcolors.ENDC
    GPIO.output(PINS["TESTEN"], False)

print bcolors.WARNING + "Loading PLL" + bcolors.ENDC
pll = si5338POST(0x70, user.osc, bus, VCOREGS, PINS["INTERRUPT"], GPIO)
time.sleep(0.5)
if pll.check():
    print bcolors.FAIL + "Exiting..." + bcolors.ENDC
    exit()
else:
    print bcolors.OKGREEN + "PLL Ready" + bcolors.ENDC

if user.jtag == True:
    print bcolors.OKGREEN + "JTAG A SELECTED" + bcolors.ENDC
    GPIO.output(PINS["JTAGSEL"], True)
else:
    print bcolors.OKGREEN + "JTAG A&B SELECTED" + bcolors.ENDC
    GPIO.output(PINS["JTAGSEL"], False)
print "BMA:",bin(int(bma))
print "BMB:",bin(int(bmb))

BMA = bunchMarker(PINS["BMASRCLK"], PINS["BMARCLK"], PINS["SRA"], GPIO)
BMB = bunchMarker(PINS["BMBSRCLK"], PINS["BMBRCLK"], PINS["SRB"], GPIO)
BMA.reset()
BMB.reset()
BMA.bunchMarker(user.bunchMarkerA)
BMB.bunchMarker(user.bunchMarkerB)


# Initialize Display

# Loading Fonts
font14h = Font("font14h")
font14h.init_bitmap("font14h.csv")
font14hL = Font("font14hL.csv")
font14hL.init_bitmap("font14hL.csv")

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
pllValue = "LOCKED"
if user.osc == 0:
    inputValue = "RF  "
else:
    inputValue = "OSC"
if user.testSignal == True:
    testCircuitValue = "ON  "
else:
    testCircuitValue = "OFF"
if user.jtag == True:
    jtagValue = "A  "
else:
    jtagValue = "AB"

#Asking for new XTD configuration
try:
    display = seps525.SEPS525_nhd(DC = PINS["DISPDC"], RES = PINS["DISPRES"], gpio = GPIO)
    display.fill_screen((255,255))
    while (True):
        # Draw Labels
        loffset = 10
        inputDisp = TS(loffset, 10, 14, inputTitle, font14h)
        bmaDisp = TS(loffset, 26, 14, bmaTitle, font14h)
        bmbDisp = TS(loffset, 42, 14, bmbTitle, font14h)
        testCircuitDisp = TS(loffset, 58, 14, testCircuitTitle, font14h)
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
        
        print "PLL Select: (0: RF or 1: OSC)"
        osc = raw_input()        
        print "\n"+"Enable Test Signal: (0: Disable or 1: Enable)"
        testSignal = raw_input()
        print "\n" + "Select JTAG: (0: A&B or 1: A)"
        jtag = raw_input()
        print "\n"+"Input new bunchMarkerA: (0 - 5280)"
        bma = raw_input()
        print "\n"+"Input new bunchMarkerB: (0 - 5280)"
        bmb = raw_input()

        user.testSignal = bool(int(testSignal))
        user.jtag = bool(int(jtag))
        user.osc = bool(int(osc))
        user.bunchMarkerA = int(bma)
        user.bunchMarkerB = int(bmb)

        print bcolors.WARNING + "Loading PLL" + bcolors.ENDC
        pll = si5338POST(0x70, user.osc, bus, VCOREGS, PINS["INTERRUPT"], GPIO)
        time.sleep(0.5)
        if user.testSignal == True:
            print bcolors.OKGREEN + "Test Signal ON " + bcolors.ENDC
            GPIO.output(PINS["TESTEN"], True)
        else:
            print bcolors.OKGREEN + "Test Signal OFF " + bcolors.ENDC
            GPIO.output(PINS["TESTEN"], False)

        if pll.check():
            print bcolors.FAIL + "Exiting..." + bcolors.ENDC
            exit()
        else:
            print bcolors.OKGREEN + "PLL Ready" + bcolors.ENDC
                                           
        if user.jtag == True:
            print bcolors.OKGREEN + "JTAG A SELECTED" + bcolors.ENDC
            GPIO.output(PINS["JTAGSEL"], True)
        else:
            print bcolors.OKGREEN + "JTAG A&B SELECTED" + bcolors.ENDC
            GPIO.output(PINS["JTAGSEL"], False)

        BMA = bunchMarker(PINS["BMASRCLK"], PINS["BMARCLK"], PINS["SRA"], GPIO)
        BMB = bunchMarker(PINS["BMBSRCLK"], PINS["BMBRCLK"], PINS["SRB"], GPIO)
        BMA.reset()
        BMB.reset()
        BMA.bunchMarker(user.bunchMarkerA)
        BMB.bunchMarker(user.bunchMarkerB)

        if pll.check():
            pllValue="NOT LOCKED!"
        else:
            pllValue="LOCKED      "

        if user.jtag == True:            
            jtagValue = "A  "
        else:
            jtagValue = "AB"

        if user.testSignal == True:
            testCircuitValue = "ON  "
        else:
            testCircuitValue = "OFF"

        bmaValue = str(user.bunchMarkerA)
        bmbValue = str(user.bunchMarkerB)
    
#shutdown protocal
    loffset = 10
    display.fill_screen((255, 255))
    shutdownDisp = TS(loffset, 26, 14, "Shutting Down", font14h)
    descDisp1 = TS(loffset, 42, 14, "Wait for Screen", font14h)
    descDisp2 = TS(loffset, 74, 14, "to Disappear", font14h)

    shutdownDisp.draw_string((0, 0), (255, 255), display)
    descDisp1.draw_string((0, 0), (255, 255), display)
    descDisp2.draw_string((0, 0), (255, 255), display)
    os.system("sudo shutdown -h now")
    print "shutting down now"


except KeyboardInterrupt:
    pass



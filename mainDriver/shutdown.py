import os
from text import Text_string as TS
import csv
from font import Font
from PINS import *

def checkShutdown(gpio = None, display = None):
    if gpio.input(PINS["TEST1"]) == False:
        loffset = 10
        display.fill_screen((255, 255))
        shutdownDisp = TS(loffset, 26, 14, "Shutting Down", font14h)
        descDisp1 = TS(loffset, 42, 14, "Wait for Screen", font14h)
        descDisp2 = TS(loffset, 74, 14, "to Disappear", font14h)

        shutdownDisp.draw_string((0, 0), (255, 255), display)
        descDisp1.draw_string((0, 0), (255, 255), display)
        descDisp2.draw_string((0, 0), (255, 255), display)
        os.system("shutdown -h now")
        return True
    else:
        return False
        
"""
font14h = Font("font14h")
font14h.init_bitmap("font14h.csv")
font14hL = Font("font14hL.csv")
font14hL.init_bitmap("font14hL.csv")


import seps525
import RPi.GPIO as GPIO
from PINS import *
GPIO.setmode(GPIO.BCM)
display = seps525.SEPS525_nhd(DC = PINS["DISPDC"], RES = PINS["DISPRES"], gpio = GPIO)
checkShutdown(display = display)
"""

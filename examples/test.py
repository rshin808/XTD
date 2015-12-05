import RPi.GPIO as gpio
from PINS import *

gpio.setmode(gpio.BCM)
gpio.setup(PINS["TESTEN"], gpio.OUT)
gpio.output(PINS["TESTEN"], True)


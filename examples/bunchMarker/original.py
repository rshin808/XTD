#!/usr/bin/env python
#Following command will print documentation of bunchMarker.py:
#pydoc bunchMarker

'''
AUTHORS:
Khan Le <khanle@hawaii.edu>
Bronson Edralin <bedralin@hawaii.edu>
Reed Shinsato <r7@hawaii.edu>
University of Hawaii at Manoa
Instrumentation Development Lab (IDLab), WAT214
    
OVERVIEW:
This is used to set bunch markers
'''

import RPi.GPIO as GPIO
import time
import sys
import os
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[96m'
    BROWN = '\033[33m'

# sets pins to gpio numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Declaring outputs for gpio Pins for bench marker A
BMA_SRCLK = 25
BMA_RCLK = 24
SR_A = 22

# Declaring outputs for gpio Pins for bench marker B
BMB_SRCLK = 23
BMB_RCLK = 27
SR_B = 17

'''
# Declaring outputs for JTAG
TMS = 14
TCK = 4
TDO = 15    #input
TDI = 18

# Declaring SCROD select, test PWR, and test  gpio PIN
SCROD_SEL = 28 
TEST_PWR = 29
TEST_1 = 9
TEST_2 = 7
'''
# Setting gpio mode
GPIO.setup(BMA_SRCLK,GPIO.OUT)
GPIO.setup(BMA_RCLK,GPIO.OUT)
GPIO.setup(SR_A,GPIO.OUT)

GPIO.setup(BMB_SRCLK,GPIO.OUT)
GPIO.setup(BMB_RCLK,GPIO.OUT)
GPIO.setup(SR_B,GPIO.OUT)
'''
GPIO.setup(TMS,GPIO.OUT)
GPIO.setup(TCK,GPIO.OUT)
GPIO.setup(TDO,GPIO.IN)
GPIO.setup(TDI,GPIO.OUT)

GPIO.setup(SCROD_SEL,GPIO.OUT)
GPIO.setup(TEST_PWR,GPIO.OUT)
GPIO.setup(TEST_1,GPIO.OUT)
GPIO.setup(TEST_2,GPIO.OUT)
'''

#Declaring functions
binary = lambda n: '' if n == 0 else binary(n/2) + str(n%2) # turns int into binary string

#Shift register clock
MAP_BOOL = {0:False,'0':False,1:True,'1':True}

def reset():
    GPIO.output(BMA_SRCLK,False)
    GPIO.output(BMA_RCLK,False)
    GPIO.output(SR_A,False)
    GPIO.output(BMB_SRCLK,False)
    GPIO.output(BMB_RCLK,False)
    GPIO.output(SR_B,False)
'''    GPIO.output(TMS,False)
    GPIO.output(TCK,False)
    GPIO.output(TDI,False)
    GPIO.output(SCROD_SEL,False)
    GPIO.output(TEST_PWR,False)
    GPIO.output(TEST_1,False)
    GPIO.output(TEST_2,False)
'''
def serial_shift(data,srd,sclk,rclk):    #Loads bit on falling edage and shifts bit on rising edge
    GPIO.setmode(GPIO.BCM)
   
    GPIO.setup(BMA_SRCLK,GPIO.OUT)
    GPIO.setup(BMA_RCLK,GPIO.OUT)
    GPIO.setup(SR_A,GPIO.OUT)

    GPIO.setup(BMB_SRCLK,GPIO.OUT)
    GPIO.setup(BMB_RCLK,GPIO.OUT)
    GPIO.setup(SR_B,GPIO.OUT)

    for data_bit in data:
        GPIO.output(srd,MAP_BOOL[data_bit])

        GPIO.output(sclk,False) # falling edge of srclk
        GPIO.output(rclk,True)  # rising edge of register clock, inverse of srclk
        GPIO.output(sclk,True)  # rising edge of srclk
        GPIO.output(rclk,False) # falling edge of register clock
    
    GPIO.output(rclk,True)
    GPIO.output(rclk,False)

    
def bunchmarker(user_a, user_b):
    bma = 65535 - user_a
    bmb = 65535 - user_b

    bma_sd = binary(bma)
    bmb_sd = binary(bmb)
    
    print "Bunch marker A shifted to register is",bma_sd
    serial_shift(bma_sd,SR_A,BMA_SRCLK,BMA_RCLK)   # shifting values out
    print bcolors.OKGREEN+"Bench Maker A shifting is complete"+bcolors.ENDC

    print "Bunch marker B shifted to register is",bmb_sd
    serial_shift(bmb_sd,SR_B,BMB_SRCLK,BMB_RCLK)
    print bcolors.OKGREEN+"Bench Marker B shifting is complete"+bcolors.ENDC


#setting up number to shift into shift register
reset()     # reseting all gpios
GPIO.cleanup()


#User input for bunch makers
print "Input Bunch Maker A"
user_a = int(sys.stdin.readline())

print "Input Bunch Marker B"
user_b = int(sys.stdin.readline())

bunchmarker(user_a, user_b)





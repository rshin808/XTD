class si5338POST:

    def __init__(self, address = None, option = False, i2c = None, regs = None, interrupt = None, gpio = None):
        self._address = address
        self._option = option
        self._BUS = i2c
        self._REGS = regs
        self._interrupt = interrupt
        self._GPIO = gpio
        self._GPIO.setmode(gpio.BCM)
        self._init()
    
    def _init(self):    
        # Setting LVDS
        self._BUS.write_byte_data(self._address, 36, 0x06)
        self._BUS.write_byte_data(self._address, 37, 0x06)
        self._BUS.write_byte_data(self._address, 40, 0x63)
        self._BUS.write_byte_data(self._address, 41, 0x8c)
        self._BUS.write_byte_data(self._address, 42, 0x23)

        # Setting PLL bypass
#        self._BUS.write_byte_data(self._address, 31, 0x08)        
        
        if self._option == False:
            self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x10)
            self._BUS.write_byte_data(self._address, self._REGS["PLLWPASS"], 0x1D)
            self._BUS.write_byte_data(self._address, self._REGS["PFDDIV"], 0x64)
            self._BUS.write_byte_data(self._address, self._REGS["PFDFB"], 0xA4)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S1"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S2"], 0x26)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S2"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S4"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S1"], 0x01)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S2"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S4"], 0x80)
            self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x0C)
            self._BUS.write_byte_data(self._address, self._REGS["PLLWPASS"], 0x00)
        else:
            self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x10)
            self._BUS.write_byte_data(self._address, self._REGS["PLLWPASS"], 0x1D)
            self._BUS.write_byte_data(self._address, self._REGS["PFDDIV"], 0x42)
            self._BUS.write_byte_data(self._address, self._REGS["PFDFB"], 0xB0)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S1"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S2"], 0x26)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S2"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S4"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S1"], 0x01)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S2"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S4"], 0x80)
            self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x0C)
            self._BUS.write_byte_data(self._address, self._REGS["PLLWPASS"], 0x00)
                                
    
        self._GPIO.setup(self._interrupt, self._GPIO.IN)
    def check(self):
        if self._GPIO.input(self._interrupt) == True:
            print "Warning LoL"
            return True
        else:
            return False         
    
    

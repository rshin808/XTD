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

class bunchMarker:
    def __init__(self, BMSRCLK = None, BMRCLK = None, SR = None, gpio = None):
        self._BMSRCLK = BMSRCLK
        self._BMRCLK = BMRCLK
        self._SR = SR
        self._GPIO = gpio
        self._binary = lambda n: '' if n == 0 else binary(n / 2) + str(n % 2)

    @property
    def BMSRCLK(self):
        return self._BMSRCLK

    @property
    def BMRCLK(self):
        return self._BMRCLK
    
    @property
    def SR(self):
        return self._SR

    def reset(self):
        self._GPIO.output(self._BMSRCLK, False)
        self._GPIO.output(self._BMRCLK, False)
        self._GPIO.output(self._SR, False)
          
    def serialShift(self, data):    #Loads bit on falling edage and shifts bit on rising edge
        self._GPIO.setup(self._BMSRCLK, self._GPIO.OUT)
        self._GPIO.setup(self._BMRCLK, self._GPIO.OUT)
        self._GPIO.setup(self._SR, self._GPIO.OUT)

        for data_bit in data:
            self._GPIO.output(self._SR, bool(int(data_bit)))
            self._GPIO.output(self._BMSRCLK, False) # falling edge of srclk
            self._GPIO.output(self._BMRCLK, True)  # rising edge of register clock, inverse of srclk
            self._GPIO.output(self._BMSRCLK, True)  # rising edge of srclk
            self._GPIO.output(self._BMRCLK, False) # falling edge of register clock
    
        self._GPIO.output(self._BMRCLK, True)
        self._GPIO.output(self._BMRCLK, False)
    
    def bunchMarker(self, value):
        bm = 65535 - value
        bmSD = self._binary(bm)
        
        self.serialShift(bm, self._SR, self._BMSRCLK, self._BMRCLK)
        print b.colors.OKGREEN + "Bench Marker shifting is complete" + bcolors.ENDC

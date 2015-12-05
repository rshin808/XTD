"""
    File: seps525.py
    By  : Reed Shinsato
    Desc: This implements the class for the basic seps525 functions.
"""

# Libraries
import spidev
import time
import csv
from font import Font

# PINS
#RS = 31
#RES = 30

#RS =  24
#RES = 25

# ADDRESSES
INDEX = 0x00
STATUS = 0x01
OSC = 0x02
I_REF = 0x80
C_DIV = 0x03
I_RED = 0x04
S_RST = 0x05
DISP_O_F = 0x06
PRE_TR = 0x08
PRE_TG = 0x09
PRE_TB = 0x0A
PRE_CR = 0x0B
PRE_CG = 0x0C
PRE_CB = 0x0D
DRI_CR = 0x10
DRI_CG = 0x11
DRI_CB = 0x12
DISP_MODE = 0x13
RGB_IF = 0x14
RGB_POL = 0x15
MEM_WM = 0x16
MX1 = 0x17
MX2 = 0x18
MX3 = 0x19
MX4 = 0x1A
MEM_ACX = 0x20
MEM_ACY = 0x21
DDRAM = 0x22
GRAY_IDX = 0x50
GRAY_DATA = 0x51
DUTY = 0x28
DSL = 0x29
D1_FAC = 0x2E
D1_FAR = 0x2F
D2_SAC = 0x31
D2_SAR = 0x32
FX1 = 0x33
FX2 = 0x34
FY1 = 0x35
FY2 = 0x36
SX1 = 0x37
SX2 = 0x38
SY1 = 0x39
SY2 = 0x3A
SS_CNTRL = 0x3B
SS_ST = 0x3C
SS_MODE = 0x3D
SCR1_FU = 0x3E
SCR1_MXY = 0x3F
SCR2_FU = 0x40
SCR2_MXY = 0x41
MOV_DIR = 0x42
SCR2_SX1 = 0x47
SCR2_SX2 = 0x48
SCR2_SY1 = 0x49
SCR2_SY2 = 0x4A

class SEPS525_nhd:
    """
        Constructor
        Param: WIDTH, The pixel width of the lcd.
               HEIGHT, The pixel height of the lcd.
               font, The font without spaces.
               font2, The font with spaces.
    """
    def __init__(self, DC = None, RES = None, WIDTH = 160, HEIGHT = 128, font = "font14h", font2 = "font14hL", gpio = None):
	    # Initialize gpio
        self._DC = DC
        self._RES = RES
        self._gpio = gpio
        self.__setup_gpio()
        self._WIDTH = WIDTH
        self._HEIGHT = HEIGHT
        self._font = Font(font)
        self._font2 = Font(font2)
        self.__seps525_init()
        self.__init_oled_display()

    """
        This sets the gpio (and spi) for the SEPS525 driver.
    """
    def __setup_gpio(self):
        global spi
        self._gpio.setup(self._RES, self._gpio.OUT)
        self._gpio.output(self._RES, True)
        self._gpio.setup(self._DC, self._gpio.OUT)
        self._gpio.output(self._DC, False)
        time.sleep(0.1)

        
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 100000000
        spi.mode = 3

    """
        This cleans up the gpio and turns off the SEPS525 driver.
    """
    def end_gpio(self):
        self._gpio.output(self._RES, True)
        self._gpio.cleanup()
        exit()


    """
        This initializes the SEPS525 driver.
    """
    def __seps525_init(self):
        # Startup RS
        self._gpio.output(self._DC, False)
        time.sleep(0.5)
        self._gpio.output(self._DC, True)
        time.sleep(0.5)
    
        # Set normal driving current
	    # Disable oscillator power down
        self.seps525_reg(I_RED, 0x01)
        time.sleep(0.002)

	    # Enable power save mode
	    # Set normal driving current
	    # Disable oscillator power down
        self.seps525_reg(I_RED, 0x00)
        time.sleep(0.002)
        
        self.seps525_reg(SS_CNTRL, 0x00)

	    # set EXPORT1 at internal clock
        self.seps525_reg(OSC, 0x01)

	    # set framerate as 120 Hz
        self.seps525_reg(C_DIV, 0x30)

	    # set reference voltage controlled by external resistor
        self.seps525_reg(I_REF, 0x01)

	    # set pre-charge time
	    # red
        self.seps525_reg(PRE_TR, 0x04)
	    # green
        self.seps525_reg(PRE_TG, 0x05)
	    # blue  
        self.seps525_reg(PRE_TB, 0x05)

    	# set pre-charge current
	    # red
        self.seps525_reg(PRE_CR, 0x9D)
	    # green
        self.seps525_reg(PRE_CG, 0x8C)
	    # blue
        self.seps525_reg(PRE_CB, 0x57)

	    # set driving current
	    # red
        self.seps525_reg(DRI_CR, 0x56)
	    # green
        self.seps525_reg(DRI_CG, 0x4D)
	    # blue 
        self.seps525_reg(DRI_CB, 0x46)

	    # set color sequence
        self.seps525_reg(DISP_MODE, 0x00)
        
	    # set MCU interface mode
        self.seps525_reg(RGB_IF, 0x01)
        self.seps525_reg(MEM_WM, 0x66)
    
	    # shift mapping RAM counter
        self.seps525_reg(MEM_ACX, 0x00)
        self.seps525_reg(MEM_ACY, 0x00)

	    # 1/128 duty
        self.seps525_reg(DUTY, 0x7F)

	    # set mapping
        self.seps525_reg(DSL, 0x00)

	    # display on
        self.seps525_reg(DISP_O_F, 0x01)

	    # disable power save mode
        self.seps525_reg(S_RST, 0x00)

    	# set RGB polarity
        self.seps525_reg(RGB_POL, 0x00)


    """
        This initializes the lcd dipslay to white.
    """
    def __init_oled_display(self):
        self.fill_screen((0, 255))
        time.sleep(0.5)


    """
        This sets the region of the lcd to draw to.
        Param: width1, The starting pixel width point. 
               height1, The starting pixel height point.
               width2, The end pixel width point.
               height2, The end pixel height point.
    """
    def seps525_set_region(self, width1 = 0, height1 = 0, width2 = 160, height2 = 128):
	    # specify the update region
	    # start on (width1, height1)
        self.seps525_reg(MX1, width1)
        self.seps525_reg(MX2, width1 + width2 - 1)
        self.seps525_reg(MX3, height1)
        self.seps525_reg(MX4, height1 + height2 -1)
        self.seps525_reg(MEM_ACX, width1)
        self.seps525_reg(MEM_ACY, height1)
    

    """
        This writes data to the SEPS525 driver.
        It is mainly for writing the pixel color data.
        Param: value, The data to write.
    """
    def data(self, value):
        global spi
        # send value
        self._gpio.output(self._DC, True)
        spi.xfer2(list(value))
        self._gpio.output(self._DC, False)
    

    """
        This writes the command address of display for the SEPS525 driver.
    """
    def data_start(self):
        global spi
        self._gpio.output(self._DC, False)
        spi.xfer([0x22])
        self._gpio.output(self._DC, True)

    
    """
        This writes a value to a specified register address of the SEPS525 driver.
        Param: address, The address of the register.
               value, The value to write to the register.
    """
    def seps525_reg(self, address, value):
        global spi
        # goto index of address and set it to value
        self._gpio.output(self._DC, False)
        spi.xfer2([address])
        self._gpio.output(self._DC, True)
        spi.xfer2([value])

    
    """
        This fills the entire screen of the lcd with a color.
        Param: color, The color to fill the screen with. 
    """
    def fill_screen(self, color):
	    # color = (c1, c2)
        self.seps525_set_region()
        self.data_start()
        value = []
	
	    # create array of 4096
        for pixel in range(2048):
            value.append(color[0])
            value.append(color[1])

	    # send data 4096 bytes each 
        for pixel in range(10):
	        self.data(value)


    """
        This draws a pixel to the lcd.
        Param: x, The x coordinate of the pixel.
               y, The y coordinate of the pixel.
               color, The color of the pixel.
    """
    def draw_pixel(self, x, y, color):
	    # color = (c1, c2)
	    self.seps525_set_region(x, y, 1, 1)
	    self.data_start()
	    self.data(list(color))

    
    """
        This draws a vertical line to the lcd.
        Param: x, The start x coordinate of the line.
               y, The start y coordinate of the line.
               h, The height of the line.
               color, The color of the line.
    """
    def draw_vline(self, x, y, h, color):
	    # color = (c1, c2)
        self.seps525_set_region(x, y, 1, h)
        self.data_start()
        value = []
        for pixel in range(h):
            value.append(color[0])
            value.append(color[1])
	
        self.data(value)


    """
        This draws a horizontal line to the lcd.
        Param: x, The start x coordinate of the line.
               y, The start y coordinate of the line.
               w, The width of the line.
               color, The color of the line.
    """
    def draw_hline(self, x, y, w, color):
	    # color = (c1, c2)
        self.seps525_set_region(x, y, w, 1)
        self.data_start()

        value = []
        for pixel in range(w):
            value.append(color[0])
            value.append(color[1])

        self.data(value)


    """
        This draws a rectangle on the lcd.
        Param: x, The start x coordinate of the rectangle.
               y, The start y coordinate of the rectangle.
               w, The width of the rectangle.
               h, The height of the rectangle.
               color, The color of the rectangle.
               filled, Whether the rectangle is filled or not.
    """
    def draw_rect(self, x, y, w, h, color, filled = True):
	    # color = (c1, c2)
        if(filled):
            self.set_region(x, y, w, h)
            self.data_start()
            value = []
            for pixel in range(2 * h * w):
                value.append(color[0])
                value.append(color[1])

            self.data(value)
        else:
            self.draw_vline(x, y, h, color)
            self.draw_hline(x, y, w, color)
            self.draw_hline(x, y + h, color)
            self.draw_vline(x + w, y, h, color)
    
    
    """
        This draws a circle to the lcd.
        Param: x, The x origin of the circle.
               y, The y origin of the circle.
               r, The radius of the circle.
               color, The color of the circle.
               filled, Whether the circle is filled or not.
    """
    def draw_circle(self, x, y, r, color, filled = False):
	    # color = (c1, c2)
        if(not filled):
            self.draw_pixel(x, y - r, color)
            self.draw_pixel(x, 2 * r + 1, color)
            f = 1 - r
            ddf_x = 1
            ddr_y = -1 * r
            x1 = 0
            y1 = r
            while (x1 < y1):
                if(f >= 0):
                    y1 -= 1
                    ddf_y += 2
                f += ddf_x
                x1 += 1
                ddf_x += 2
                f += ddf_x
                self.draw_pixel((x + x1), (y - y1), color)
                self.draw_pixel((x + x1), (y + y1), color)
                self.draw_pixel((x + y1), (y - x1), color)
                self.draw_pixel((x + y1), (y + x1), color)
                self.draw_pixel((x - x1), (y - y1), color)
                self.draw_pixel((x - x1), (y + y1), color)
                self.draw_pixel((x - y1), (y - x1), color)
                self.draw_pixel((x - y1), (y + x1), color)
   

    """
        This tells the SEPS525 driver to turn on the display.
    """
    def show(self):
        self.seps525_reg(DISP_O_F, 0x01)
     

    """
        This tells the SEPS525 driver to turn off the display.
    """
    def hide(self):
        self.seps525_reg(DISP_O_F, 0x00)


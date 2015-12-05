from font import Font

font14h = Font("font14h")
font14h.init_bitmap("font14h.csv")

class Text_string:
    def __init__(self, x, y, height, string, font):
        self._string = string.replace(" " , "|")
        self._bitmap = []
        self._height = height
        self._x = x
        self._y = y
        self._len = 0
        self._font = font
        self.__init_bitmap(self._font)
    def __str__(self):
        return str(self._string).replace("|", " ")

    def __len__(self):
        return self._len

    def __init_bitmap(self, font):
        self._bitmap = []
        for h in range(self._height):
            self._bitmap.append("")
            for c in self._string:
                self._bitmap[h] += font.FONT[c][h]
        self._len = len(self._bitmap[0])
    
    def update_string(self, string):
        string = string.replace(" ", "|")
        remaining = len(string) - len(self._string)
        if remaining > 0:
            for check in range(remaining):
                string += "|"
        self._string = string
        self.__init_bitmap(self._font)

    def draw_string(self, color, background, oled):
        oled.seps525_set_region(self._x, self._y, self._len, self._height)
        oled.data_start()
        value = []
        for h in range(self._height):
            for c in self._bitmap[h]:
                if c == "0":
                    value.append(background[0])
                    value.append(background[1])
                else:
                    value.append(color[0])
                    value.append(color[1])
        repeats = int(len(value) / 4096)
        remainder = len(value) % 4096
        for v in range(repeats):
            oled.data(value[4096 * v:4096 * v + 4095])
        oled.data(value[repeats * 4096:])  

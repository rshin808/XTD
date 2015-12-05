import os
import csv
class Font:
    # LIBRARIES

    """
	Reads a font from a csv bitmap.
    """
    def __init__(self, name, spacer = 2):
        self._name = name
        self.FONT = {}
        self._spacer = ""
        for i in range(spacer):
            self._spacer += "0"

    def __str__(self):
        characters = ""
        for char in self.FONT:
            characters += char
        return characters

    def init_bitmap(self, input_file):
	"""
	    Initialize the bitmap from csv file.
	    The csv row should consist of name, string of 1's and 0's(of width).
	    Use fontparser.py to get the .csv.
	"""
        script_path = os.path.dirname(os.path.realpath(__file__))
        input_file_path = os.path.join(script_path, input_file)
        with open(input_file_path, "rb") as bitmap_file:
            reader = csv.reader(bitmap_file)
            for row in reader:
                if row[0] not in self.FONT.keys():
                    self.FONT[str(row[0])] = []
                    self.FONT[str(row[0])].append(row[1] + self._spacer)
                else:
                    self.FONT[str(row[0])].append(row[1] + self._spacer)

import csv
import smbus

i2c = smbus.SMBus(1)

reg = 400
filename = "SIREGValues.txt"
with open(filename, "wb") as outputFile:
    outWriter = csv.writer(outputFile)
    for i in range(reg):
        outRow = [i, hex(i2c.read_byte_data(0x70, i))]
        outWriter.writerow(outRow) 

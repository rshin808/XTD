#!/usr/bin/env python

import os
import csv

def getIP():
    try:
        os.system("ifconfig eth0 > IPADDRESS.txt")
        line = []

        with open("IPADDRESS.txt", "rb") as IP:
            csvReader = csv.reader(IP)
            for row in csvReader:
                if row != []:
                    if "inet addr:" in row[0]:
                        line = row[0]

        line = line.split("inet addr:")
        return line[1].split()[0]
    except:
        return "No IP         "

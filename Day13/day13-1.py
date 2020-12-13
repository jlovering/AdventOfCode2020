#!/bin/python

import sys
import copy
import re
import math

infile = open(sys.argv[1], "r")

class Bus:
    def __init__(self, ID):
        self.id = ID

    def __str__(self):
        return "%d" % self.id

    def nextArrival(self, time):
        previousArr = math.floor(time/self.id) * self.id
        return previousArr + self.id

    def getID(self):
        return self.id

arrivalTime = 0
busses = []

arrivalTime = int(infile.readline().rstrip())
busList = infile.readline().rstrip().split(',')

#print(arrivalTime, busList)

for busID in busList:
    if busID == 'x':
        continue;

    busses.append(Bus(int(busID)))

busArrivals = [ (b.getID(), b.nextArrival(arrivalTime)) for b in busses ]

print(busArrivals)
(ID, time) = min(busArrivals, key=lambda i: i[1])

print(ID, time)

print ((time - arrivalTime) * ID)
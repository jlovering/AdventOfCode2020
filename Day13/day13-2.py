#!/bin/python

import sys
import copy
import re
import math

infile = open(sys.argv[1], "r")

class Bus:
    def __init__(self, ID, ord):
        self.id = ID
        self.ord = ord

    def __str__(self):
        return "%d: %d" % (self.ord, self.id)

    def nextArrival(self, time):
        previousArr = math.floor(time/self.id) * self.id
        return previousArr + self.id

    def isArrival(self, time):
        return time % self.id == 0

    def getID(self):
        return self.id

    def getOrd(self):
        return self.ord

arrivalTime = 0
busses = []

arrivalTime = int(infile.readline().rstrip())
busList = infile.readline().rstrip().split(',')

#print(arrivalTime, busList)

for (busID, ord) in zip(busList, range(len(busList))):
    if busID == 'x':
        continue;

    busses.append(Bus(int(busID), int(ord + 0)))

def checkContest(time, busses):
    for b in busses:
        #print("\t", b.getOrd(), b.getID())
        if not b.nextArrival(time-1) == time + b.getOrd():
            return False
    return True

#sort by ID largest to smalles, this is a smaller search space
#busses.sort(key=lambda b: b.getID())

print([str(b) for b in busses])

t_cand = 1
superCycle = 1
for b in busses:
    while not b.isArrival(t_cand + b.getOrd()):
        t_cand += superCycle
    superCycle *= b.getID()

print(t_cand)

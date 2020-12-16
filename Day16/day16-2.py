#!/bin/python

import sys
import copy
import re

infile = open(sys.argv[1], "r")

class Validator:
    def __init__(self, name):
        self.name = name
        self.ranges = []

    def addRule(self, minV, maxV):
        self.ranges.append((minV,maxV))

    def checkAllRanges(self, value):
        for r in self.ranges:
            if value >= r[0] and value <= r[1]:
                return True
        return False

    def getName(self):
        return self.name

    def __str__(self):
        return "%d - %d or %d - %d" % (self.ranges[0][0], self.ranges[0][1], self.ranges[1][0], self.ranges[1][1])

class Ticket:
    def __init__(self, fields):
        self.fields = fields

    def getFields(self):
        return self.fields

    def __str__(self):
        return str(self.fields)

valitators = []
myTicket = None
otherTickets = []

def parseTicket(line):
    fs = line.split(',')
    return Ticket([int(f) for f in fs])

def inputParse(file):
    global valitators, myTicket, otherTickets
    line = infile.readline().rstrip()

    while line != "":
        #Get the rules
        lineM = re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", line)
        if lineM is None:
            raise Exception("Bad match:\"%s\"" % line)
        v = Validator(lineM.group(1))
        v.addRule(int(lineM.group(2)), int(lineM.group(3)))
        v.addRule(int(lineM.group(4)), int(lineM.group(5)))

        valitators.append(v)

        line = infile.readline().rstrip()

    line = infile.readline().rstrip()
    if line != "your ticket:":
        raise Exception("Malformed")

    line = infile.readline().rstrip()
    myTicket = parseTicket(line)

    line = infile.readline().rstrip()
    line = infile.readline().rstrip()
    if line != "nearby tickets:":
        raise Exception("Malformed")

    line = infile.readline().rstrip()
    while line and line != "":
        otherTickets.append(parseTicket(line))
        line = infile.readline().rstrip()

inputParse(infile)

invalidTickets = []
for t in otherTickets:
    for f in t.getFields():
        valitatorsResults = [ v.checkAllRanges(f) for v in valitators ]
        #print(f, valitatorsResults)
        if True not in valitatorsResults:
            invalidTickets.append(t)
            break

for t in invalidTickets:
    otherTickets.remove(t)

validatorPos = {}
for v in valitators:
    for (i, _) in enumerate(myTicket.getFields()):
        #print (i)
        valids = []
        for t in otherTickets:
            #print (str(t))
            valids.append(v.checkAllRanges(t.getFields()[i]))
        if False not in valids:
            if v.getName() in validatorPos:
                validatorPos[v.getName()].append(i)
            else:
                validatorPos[v.getName()] = [i]

print (validatorPos)

finalPos = {}

while len(finalPos) != len(validatorPos):
    for v in validatorPos:
        if len(validatorPos[v]) == 1:
            #print("culling")
            known = validatorPos[v][0]
            finalPos[v] = known
            for r in validatorPos:
                if r == v:
                    continue
                if known in validatorPos[r]:
                    validatorPos[r].remove(known)

print (finalPos)

product = 1
for f in [ v.getName() for v in valitators ]:
    #print(f)
    if "departure" in f:
        print(f, finalPos[f], myTicket.getFields()[finalPos[f]])
        product *= myTicket.getFields()[finalPos[f]]

print (product)
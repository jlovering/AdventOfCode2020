#!/bin/python

import sys
import copy
import re
import math

infile = open(sys.argv[1], "r")

instructions = []

for line in infile:
    line = line.rstrip()

    lineM = re.match(r"(N|S|E|W|L|R|F)(\d+)", line)
    if not lineM:
        print("poop")

    instructions.append((lineM.group(1), int(lineM.group(2))))

#print(instructions)

class Waypoint:
    def __init__(self, startDir):
        self.ewpos = 10
        self.nspos = 1

    def execute_N(self, value):
        self.nspos += value

    def execute_S(self, value):
        self.nspos -= value

    def execute_E(self, value):
        self.ewpos += value

    def execute_W(self, value):
        self.ewpos -= value

    def genericRotate(self, value):
        cth = round(math.cos(value))
        sth = round(math.sin(value))
        ewpos = int(self.ewpos * cth - self.nspos * sth)
        nspos = int(self.ewpos * sth + self.nspos * cth)

        self.ewpos = ewpos
        self.nspos = nspos

    def execute_L(self, value):
        self.genericRotate(math.radians(value))

    def execute_R(self, value):
        value *= -1
        self.genericRotate(math.radians(value))

    def executeInstruction(self, instruction):
        (action, value) = instruction

        #print(instruction, self.ewpos, self.nspos)
        eval("self.execute_%s(%d)" % (action, value))
        #print("\t", self.ewpos, self.nspos)

    def getVector(self):
        return (self.ewpos, self.nspos)

class Ship:
    def __init__(self):
        self.ewpos = 0
        self.nspos = 0
        self.waypoint = Waypoint(90)

    def execute_F(self, value):
        (wewpos, wnspos) = self.waypoint.getVector()
        self.ewpos += wewpos * value
        self.nspos += wnspos * value

    def executeInstruction(self, instruction):
        (action, value) = instruction

        #print(instruction, self.ewpos, self.nspos)
        if action == 'F':
            self.execute_F(value)
        else:
            self.waypoint.executeInstruction(instruction)
        #print(instruction, self.ewpos, self.nspos)

    def computeManhattan(self):
        return (abs(self.nspos) + abs(self.ewpos))

ship = Ship()

for instruction in instructions:
    ship.executeInstruction(instruction)

print(ship.computeManhattan())
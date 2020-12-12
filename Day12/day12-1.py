#!/bin/python

import sys
import copy
import re

infile = open(sys.argv[1], "r")

instructions = []

for line in infile:
    line = line.rstrip()

    lineM = re.match(r"(N|S|E|W|L|R|F)(\d+)", line)
    if not lineM:
        print("poop")

    instructions.append((lineM.group(1), int(lineM.group(2))))

#print(instructions)

class Ship:
    def __init__(self, startDir):
        self.heading = startDir
        self.ewpos = 0
        self.nspos = 0

    def execute_N(self, value):
        self.nspos += value

    def execute_S(self, value):
        self.nspos -= value

    def execute_E(self, value):
        self.ewpos += value

    def execute_W(self, value):
        self.ewpos -= value

    def execute_L(self, value):
        if value > self.heading:
            self.heading = 360 - (value-self.heading)
        else:
            self.heading -= value

    def execute_R(self, value):
        self.heading += value
        self.heading %= 360

    def execute_F(self, value):
        if self.heading % 90 != 0:
            raise Exception("Angle not cardinal: %d (%d)", self.heading)

        if self.heading == 0 or self.heading == 360:
            self.execute_N(value)
        elif self.heading == 90:
            self.execute_E(value)
        elif self.heading == 180:
            self.execute_S(value)
        elif self.heading == 270:
            self.execute_W(value)
        else:
            raise Exception("Angle not cardinal")

    def executeInstruction(self, instruction):
        (action, value) = instruction

        #print(instruction, self.heading, self.ewpos, self.nspos)
        eval("self.execute_%s(%d)" % (action, value))
        #print("\t", self.heading, self.ewpos, self.nspos)

    def computeManhattan(self):
        return (abs(self.nspos) + abs(self.ewpos))

ship = Ship(90)

for instruction in instructions:
    ship.executeInstruction(instruction)

print(ship.computeManhattan())
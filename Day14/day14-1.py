#!/bin/python

import sys
import copy
import re

infile = open(sys.argv[1], "r")

instructions = []

class Memory:
    def __init__(self):
        self.memory = {}
        self.maskOut = 0
        self.replaceMask = 0

    def setMask(self, maskString):
        nibbler = 0
        self.maskOut = 0
        self.replaceMask = 0
        thisMaskOut = 0
        thisreplaceMask = 0
        #print(maskString)
        for c in maskString:
            #print("%s\t0x%01X 0x%01X" % (c, thisMaskOut, thisreplaceMask))
            if c == 'X':
                thisMaskOut |= 0x1
            elif c == '1':
                thisMaskOut |= 0x0
                thisreplaceMask |= 0x1
            elif c == '0':
                thisMaskOut |= 0x0
                thisreplaceMask |= 0x0

            #print("%s\t0x%01X 0x%01X" % (c, thisMaskOut, thisreplaceMask))
            nibbler += 1
            #print("%s\t0x%01X 0x%01X %d" % (c, thisMaskOut, thisreplaceMask, nibbler))

            if nibbler != 0 and nibbler % 4 == 0:
                #print("nibble")
                self.maskOut <<= 4
                self.maskOut |= thisMaskOut & 0xF
                self.replaceMask <<= 4
                self.replaceMask |= thisreplaceMask & 0xF
                thisMaskOut = 0
                thisreplaceMask = 0
            else:
                thisMaskOut <<= 1
                thisreplaceMask <<= 1
        #print("0x%09X 0x%09X" % (self.maskOut, self.replaceMask))

    def maskAndWrite(self, location, value):
        value &= self.maskOut
        value |= self.replaceMask

        #print(location, value)
        self.memory[location] = value

    def dumpMemory(self):
        return self.memory.values()

memory = Memory()

for line in infile:
    line = line.rstrip()


    lineM = re.match(r"mask = ([0,1,X]{36})", line)
    if lineM:
        instructions.append(("MASK", lineM.group(1)))
        continue

    lineM = re.match(r"mem\[(\d+)\] = (\d+)", line)
    if lineM:
        instructions.append(("WRITE", int(lineM.group(1)), int(lineM.group(2))))
        continue

for i, *v in instructions:
    if i == "MASK":
        memory.setMask(v[0])
    elif i == "WRITE":
        memory.maskAndWrite(v[0], v[1])
    else:
        print("oops")

print(sum(memory.dumpMemory()))

#!/bin/python

import sys
import copy
import re

infile = open(sys.argv[1], "r")

instructions = []

class Memory:
    def __init__(self):
        self.memory = {}
        self.maskString = ""

    def setMask(self, maskString):
        self.maskString = maskString

    def maskedAddresses(self, address):
        addressString = "{0:036b}".format(address)
        def addValueToAddress(addresses, value):
            tempAddresses = copy.copy(addresses)
            for (i, a) in enumerate(tempAddresses):
                tempAddresses[i] = a + value
            return tempAddresses

        allAddress = [""]
        for (abit, mbit) in zip(addressString, self.maskString):
            if mbit == '0':
                allAddress = addValueToAddress(allAddress, abit)
            elif mbit == '1':
                allAddress = addValueToAddress(allAddress, '1')
            elif mbit == 'X':
                zeroPath = addValueToAddress(allAddress, '0')
                onesPath = addValueToAddress(allAddress, '1')
                allAddress = zeroPath + onesPath
            else:
                raise Exception("Pooped the mask")

            #print(abit, mbit, end='')
            #for a in allAddress:
            #    print("\t", a)

        return [int(a, 2) for a in allAddress]

    def maskAndWrite(self, location, value):
        addresses = self.maskedAddresses(location)

        #addresses.sort()
        for a in addresses:
            #print("%s = %d" % (a, value))
            self.memory[a] = value

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

#!/bin/python

import sys
import re

infile = open(sys.argv[1], "r")

program = []

lineNo = 1
for line in infile:
    line = line.rstrip()

    lineRE = re.match(r"(acc|jmp|nop) (\+|-)(\d+)", line)

    if not lineRE:
        print "SHIT"

    argument = int(lineRE.group(3))
    if lineRE.group(2) == '-':
        argument *= -1

    program.append((lineNo, lineRE.group(1), argument))
    lineNo += 1

print program
accumulator = 0
programCounter = 0
runLines = []

while True:
    (line, inst, arg) = program[programCounter]

    if line in runLines:
        print "Revisting %d: acc: %d" % (line, accumulator)
        break;

    if inst == "acc":
        accumulator += arg
        programCounter += 1
    elif inst == "jmp":
        programCounter += arg
    elif inst == "nop":
        nop = 0
        programCounter += 1
    else:
        print "Bugger"

    runLines.append(line)
    print line, inst, arg, programCounter, accumulator
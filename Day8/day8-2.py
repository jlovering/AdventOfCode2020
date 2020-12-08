#!/bin/python

import sys
import re
import copy

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

def runProgram(program):
    accumulator = 0
    programCounter = 0
    runLines = []

    #print program
    while True:
        (line, inst, arg) = program[programCounter]

        if line in runLines:
            print "Revisting %d: acc: %d" % (line, accumulator)
            return False

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

        if programCounter >= len(program):
            print "Terminated acc: %d" % accumulator
            return True

        runLines.append(line)
        #print line, inst, arg, programCounter, accumulator

if (runProgram(program)):
        sys.exit()

for line in [line for (line, inst, _) in program if inst == 'jmp']:
    testProgram = copy.deepcopy(program)
    (lineNo, inst, arg) = testProgram[line-1]
    testProgram[line-1] = (lineNo, 'nop', arg)
    print "Modify: %d jmp" % line
    if (runProgram(testProgram)):
        sys.exit()

for line in [line for (line, inst, _) in program if inst == 'nop']:
    testProgram = copy.deepcopy(program)
    (lineNo, inst, arg) = testProgram[line-1]
    testProgram[line-1] = (lineNo, 'jmp', arg)
    print "Modify: %d nop" % line
    if (runProgram(testProgram)):
        sys.exit()
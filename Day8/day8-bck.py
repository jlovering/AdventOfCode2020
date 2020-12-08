#!/bin/python

import sys
import re
import copy

infile = open(sys.argv[1], "r")

program = []

for line in infile:
    line = line.rstrip()

    lineRE = re.match(r"(acc|jmp|nop) (\+|-)(\d+)", line)

    if not lineRE:
        print "SHIT"

    argument = int(lineRE.group(3))
    if lineRE.group(2) == '-':
        argument *= -1

    program.append((lineRE.group(1), argument))

class Processor:

    def __init__(self, program):
        self.program = program
        self.programCounter = 0
        self.accumulator = 0
        self.linesRun = []
        self.stack = []
        self.mutation = None

    def checkFault(self):
        return self.programCounter in self.linesRun

    def checkTerminated(self):
        return self.programCounter == len(self.program)

    def pushStack(self):
        self.stack.append((self.programCounter, self.accumulator, self.linesRun))

    def popStack(self):
        (self.programCounter, self.accumulator, self.linesRun) = self.stack.pop()

    def isMutant(self):
        if self.mutation is not None:
            return True
        return False

    def mutate(self):
        (inst, arg) = self.program[self.programCounter]

        mutation = (self.programCounter, inst, arg)

        if inst == 'jmp':
            inst = 'nop'
        elif inst == 'nop':
            inst = 'jmp'
        else:
            return False

        self.mutation = mutation

        self.program[self.programCounter] = (inst, arg)

        return True

    def unmutate(self):
        (pc, inst, arg) = self.mutation
        self.program[pc] = (inst, arg)

        while self.programCounter != pc:
            self.popStack()

        self.mutation = None

    def nextInstruction(self):
        (inst, arg) = self.program[self.programCounter]
        self.linesRun.append(self.programCounter)
        print self.programCounter, inst, arg
        self.pushStack()
        eval("self." + str(inst) + "(" + str(arg) + ")")

    def acc(self, arg):
        self.accumulator += arg
        self.programCounter += 1

    def jmp(self, arg):
        self.programCounter += arg

    def nop(self, arg):
        self.programCounter += 1

    def runProgram(self):
        #print program
        while True:

            if self.checkFault():
                print "Fault: %d acc %d" % (self.programCounter, self.accumulator)
                if self.isMutant():
                    self.unmutate()

                self.popStack()
                while (not self.mutate()):
                    self.popStack()

            self.nextInstruction()

            if self.checkTerminated():
                print "Terminated: %d acc %d" % (self.programCounter, self.accumulator)
                if self.isMutant():
                    print "Mutated: %d %s %d" % self.mutation
                return True

thisMachine = Processor(program)
thisMachine.runProgram()
sys.exit()
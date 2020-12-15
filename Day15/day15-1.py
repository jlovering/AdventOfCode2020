#!/bin/python

import sys
import copy
import re

infile = open(sys.argv[1], "r")

class Game:
    def __init__(self):
        self.memory = {}

    def setMemory(self, numbers):
        for (i, n) in enumerate(numbers):
            self.memory[n] = i + 1

    def speakNumber(self, lastNumber, n):
        #print(n, lastNumber)
        if lastNumber in self.memory:
            lastSpokenidx = self.memory[lastNumber]
            #print("\t", lastSpokenidx)
            self.memory[lastNumber] = n
            return n - lastSpokenidx
        else:
            self.memory[lastNumber] = n
            return 0

game = Game()
lastSpoken = 0
n = 1

for line in infile:
    line = line.rstrip()

    numbers = [ int(i) for i in line.split(',') ]

    game.setMemory(numbers)

    lastSpoken = numbers[-1]
    n += len(numbers)

    #print (numbers)

while n <= 2020:
    lastSpoken = game.speakNumber(lastSpoken, n-1)
    #print(lastSpoken)
    n += 1

print(n, lastSpoken)
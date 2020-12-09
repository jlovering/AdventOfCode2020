#!/bin/python

import sys

PREAMBLE_LEN = 25
from itertools import combinations

infile = open(sys.argv[1], "r")

input = []

lineNo = 1
for line in infile:
    line = line.rstrip()

    input.append(int(line))

def findNonMatching(input):
    rollingWindow = input[0:PREAMBLE_LEN]
    message = input[PREAMBLE_LEN:-1]
    for c in message:
        valid = [ x + y for (x,y) in list(combinations(rollingWindow,2))]

        if c not in valid:
            print "Invalid number: ", c
            return c

        rollingWindow.pop(0)
        rollingWindow.append(c)

def findLongestContineousPos(input, number):
    start = 0
    end = 1
    sumS = input[0] + input[1]

    while sumS != number:
        if sumS < number:
            end += 1
            sumS += input[end]
        if sumS > number:
            sumS -= input[start]
            start += 1

    return start, end

def findSmallLargeSum(input, start, end):
    numSet = input[start:end]
    numSet.sort()
    return numSet[0] + numSet[-1]

N = findNonMatching(input)
start, end = findLongestContineousPos(input, N)
print findSmallLargeSum(input, start, end)
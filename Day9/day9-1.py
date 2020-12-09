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

rollingWindow = input[0:PREAMBLE_LEN]
message = input[PREAMBLE_LEN:-1]

for c in message:
    valid = [ x + y for (x,y) in list(combinations(rollingWindow,2))]

    if c not in valid:
        print "Invalid number: ", c

    rollingWindow.pop(0)
    rollingWindow.append(c)
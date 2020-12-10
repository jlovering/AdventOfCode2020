#!/bin/python

import sys

infile = open(sys.argv[1], "r")

input = []

lineNo = 1
for line in infile:
    line = line.rstrip()

    input.append(int(line))

input.sort()
input.append(input[-1] + 3)

oneJolt = 0
twoJolt = 0
threeJolt = 0

#print input

prev = 0
for a in input:
    #print prev, a
    if a - prev == 1:
        oneJolt += 1
    elif a - prev == 2:
        twoJolt +=1
    elif a - prev == 3:
        threeJolt +=1
    prev = a

    #print "\t", oneJolt, twoJolt, threeJolt

print oneJolt, twoJolt, threeJolt, oneJolt*threeJolt
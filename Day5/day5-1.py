#!/bin/python

import sys

def convertCodetoNumber(s, Cone):
    value = 0
    for c in s:
        #print "\t", c
        value = value*2
        if c == Cone:
            value += 1
        #print "\t\t", value
    return value

infile = open(sys.argv[1], "r")

maxId = 0

for line in infile:
    line = line.rstrip()

    row = line[0:7]
    seat = line[7:10]

    rowN = convertCodetoNumber(row, 'B')
    seatN = convertCodetoNumber(seat, 'R')

    print line, row, seat, rowN, seatN, (rowN * 8 + seatN)

    maxId = max(maxId, (rowN * 8 + seatN))

print maxId
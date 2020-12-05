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

ids = []

for line in infile:
    line = line.rstrip()

    row = line[0:7]
    seat = line[7:10]

    rowN = convertCodetoNumber(row, 'B')
    seatN = convertCodetoNumber(seat, 'R')

    #print line, row, seat, rowN, seatN, (rowN * 8 + seatN)

    ids.append((rowN * 8 + seatN))

ids.sort()

prefectIds = [x for x in range(ids[0],ids[-1])]

print [y for y in prefectIds if y not in ids][0]

#for (idx, value) in zip(range(1,len(ids)-1), range(ids[1], ids[-2])):
#    if (ids[idx-1] != ids[idx]-1 or ids[idx+1] != ids[idx]+1):
#        print idx, ids[idx], ids[idx-1], ids[idx+1]
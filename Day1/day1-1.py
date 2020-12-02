#!/bin/python

import sys

numbers = []

infile = open(sys.argv[1], "r")

for line in infile:
    numbers.append(int(line.rstrip()))

numbers.sort()

lidx = 0
ridx = 1
lnum = numbers[lidx]
rnum = numbers[-ridx]

lidx = 1
ridx = 2
while (lnum + rnum != 2020):
    if (lnum + rnum < 2020):
        lnum = numbers[lidx]
        lidx += 1
    else:
        rnum = numbers[-ridx]
        ridx += 1
    print lnum, lidx, rnum, ridx

print lnum, rnum, lnum + rnum, lnum * rnum
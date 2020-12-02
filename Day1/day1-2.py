#!/bin/python

import sys

numbers = []

infile = open(sys.argv[1], "r")

for line in infile:
    numbers.append(int(line.rstrip()))

numbers.sort()

lidx = 0
midx = 1
ridx = -1
lnum = numbers[lidx]
mnum = numbers[midx]
rnum = numbers[ridx]

lidx = 0
midx = 2
ridx = -1

while (lnum + mnum + rnum != 2020):
    if (lnum + mnum + rnum < 2020):
        while (lnum + mnum + rnum != 2020) and midx < (len(numbers) + ridx):
            mnum = numbers[midx]
            midx += 1
        if midx < (len(numbers) + ridx):
            break
        else:
            lnum = numbers[lidx]
            lidx += 1
            midx = lidx +1
            mnum = numbers[midx]
    else:
        rnum = numbers[ridx]
        ridx -= 1
        lidx = 0
        midx = 1
    print lnum, mnum, rnum, lidx, midx, ridx

print lnum, mnum, rnum, lnum + mnum + rnum, lnum * mnum * rnum
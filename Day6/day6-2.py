#!/bin/python

import sys

def process(current):
    allYes = [x for x in current.keys() if x != 'count' and current[x] == current['count']]
    print current, allYes
    return len(allYes)

groupCount = []

infile = open(sys.argv[1], "r")

current = {}
count = 0
for line in infile:
    line = line.rstrip()

    if line == "":
        current['count'] = count
        groupCount.append(process(current))
        current = {}
        count = 0
        continue

    for c in line:
        if current.has_key(c):
            current[c] += 1
        else:
            current[c] = 1
    count += 1

print sum(groupCount)
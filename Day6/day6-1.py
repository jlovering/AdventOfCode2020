#!/bin/python

import sys

def process(current):
    print current
    return len(current.keys())

groupCount = []

infile = open(sys.argv[1], "r")

current = {}
for line in infile:
    line = line.rstrip()

    if line == "":
        groupCount.append(process(current))
        current = {}

    for c in line:
        if current.has_key(c):
            current[c] += 1
        else:
            current[c] = 1

print sum(groupCount)
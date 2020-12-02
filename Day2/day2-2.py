#!/bin/python

import sys

passwords = []

infile = open(sys.argv[1], "r")

for line in infile:
    line = line.rstrip()
    parse = line.split(' ')
    ruleRange = parse[0].split('-')
    rule = parse[1][0]
    password = parse[2]
    passwords.append((int(ruleRange[0]),int(ruleRange[1]),rule,password))

valid = 0
invalid = 0

for (rMin, rMax, rule, password) in passwords:
    count = 0
    for (i, c) in zip(range(1, len(password) + 1), password):
        if c == rule and (i == rMin or i == rMax):
            count +=1
    if count == 1:
        valid += 1
    else:
        invalid += 1

print valid, invalid
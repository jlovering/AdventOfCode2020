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
    for c in password:
        if c == rule:
            count +=1
    if count >= rMin and count <= rMax:
        valid += 1
    else:
        invalid += 1

print valid, invalid
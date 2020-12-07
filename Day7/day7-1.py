#!/bin/python

import sys
import re

infile = open(sys.argv[1], "r")

ruleMap = {}

for line in infile:
    line = line.rstrip()

    parts = line.split(" bags contain")
    ruleFor = parts[0]

    if parts[1] == " no other bags.":
        ruleMap[ruleFor] = 'Empty'
        continue

    ruleMap[ruleFor] = {}

    rules = parts[1].split(",");
    for rule in rules:
        parser = re.match(r"[\s]*(\d+) (.+) bag[s]{0,1}", rule)
        #if parser is not None:
        #    print rule, parser.group(1), parser.group(2)

        ruleMap[ruleFor][parser.group(2)] = parser.group(1)

print ruleMap

pathstoSGB = 0

for type in ruleMap:
    visited = [type]
    checklist = []

    if isinstance(ruleMap[type], dict):
        checklist += ruleMap[type].keys()
    print checklist
    while len(checklist) != 0:
        check = checklist.pop()
        if check == 'shiny gold':
            pathstoSGB += 1
            break
        visited.append(check)
        if isinstance(ruleMap[check], dict):
            checklist += [ rule for rule in ruleMap[check].keys() if rule not in visited]
        print "\t", checklist

print pathstoSGB
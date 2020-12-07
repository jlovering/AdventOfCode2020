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
        ruleMap[ruleFor] = 0
        continue

    ruleMap[ruleFor] = {}

    rules = parts[1].split(",");
    for rule in rules:
        parser = re.match(r"[\s]*(\d+) (.+) bag[s]{0,1}", rule)
        #if parser is not None:
        #    print rule, parser.group(1), parser.group(2)

        ruleMap[ruleFor][parser.group(2)] = int(parser.group(1))

print ruleMap

def requiredToContain(type):
    required = 0
    #print type, ruleMap[type], isinstance(ruleMap[type], dict)
    if isinstance(ruleMap[type], dict):
        for k in ruleMap[type].keys():
            required += requiredToContain(k) * ruleMap[type][k] + ruleMap[type][k]
    return required

numberOfBags = requiredToContain('shiny gold')

print numberOfBags
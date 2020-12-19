#!/bin/python

import sys
import copy
import re
import itertools

def parseRules(infile):

    rules = {}
    baseRules = []

    line = infile.readline().rstrip()
    while line != "":
        lineM = re.match(r"(\d+): (.*)", line)
        if lineM is None:
            raise Exception("Bad Rule")

        (idx, value) = (int(lineM.group(1)), lineM.group(2).split(" | "))
        if len(value) == 1:
            valM = re.match(r"\"(.*)\"", value[0])
            if valM:
                baseRules.append(idx)
                rules[idx] = [[valM.group(1)]]
            else:
                rules[idx] = [list(map(int, v.split(' '))) for v in value]
        else:
            rules[idx] = [list(map(int, v.split(' '))) for v in value]

        line = infile.readline().rstrip()

    return (rules, baseRules)

#def distributeAll(arr1, arr2):
#    allT = []
#    #print(arr1, arr2)
#    for a in arr1:
#        for b in arr2:
#            allT.append(a+b)
#    return allT

solvedStrings = {}
def expandRule(idx, rules, baseRules):
    #print(idx)
    if idx in solvedStrings:
        return solvedStrings[idx]
    if idx in baseRules:
        return rules[idx][0]
    strings = []
    r = rules[idx]
    for branch in r:
        subruleStrings = []
        for subrules in branch:
            subruleStrings.append(expandRule(subrules, rules, baseRules))

        #print(idx, subruleStrings)

        for ss in itertools.product(*subruleStrings):
            strings += [''.join(ss)]

    solvedStrings[idx] = strings
    return strings

def expandRule0(rules, baseRules):
    return expandRule(0, rules, baseRules)

def parseMessages(infile, rule0Strings):
    count = 0
    line = infile.readline().rstrip()

    while line != "":
        if line in rule0Strings:
            count += 1
        line = infile.readline().rstrip()

    return count

infile = open(sys.argv[1], "r")

(rules, baseRules) = parseRules(infile)

#print(rules, baseRules)

rule0Strings = expandRule0(rules, baseRules)

#print(rule0Strings)

print(parseMessages(infile, rule0Strings))
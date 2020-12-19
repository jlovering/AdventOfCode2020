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

def specialRule8(rules, baseRules):
    rule42 = expandRule(42, rules, baseRules)
    solvedStrings[8] = "(" + rule42 + "+" + ")"
    return "(" + rule42 + "+" + ")"

MAXRULE11 = 10
def specialRule11(rules, baseRules):
    rule42 = expandRule(42, rules, baseRules)
    rule31 = expandRule(31, rules, baseRules)

    stringRE = "("
    for i in range(MAXRULE11):
        stringRE += rule42*(i+1) + rule31*(i+1) + "|"

    stringRE = stringRE[:-1] + ")"
    solvedStrings[11] = stringRE
    return stringRE

def expandRule(idx, rules, baseRules):
    #print(idx)
    if idx in solvedStrings:
        return solvedStrings[idx]
    if idx in baseRules:
        return rules[idx][0][0]
    if idx == 8:
        return specialRule8(rules, baseRules)
    if idx == 11:
        return specialRule11(rules, baseRules)
    r = rules[idx]
    stringRE = "("
    for branch in r:
        subruleStrings = []
        for subrules in branch:
            subruleStrings.append(expandRule(subrules, rules, baseRules))

        #print(idx, subruleStrings)
        stringRE += ''.join(subruleStrings) + "|"

    stringRE = stringRE[:-1] + ")"
    #print(idx, stringRE)
    solvedStrings[idx] = stringRE
    return stringRE

def parseMessages(infile):
    count = 0
    line = infile.readline().rstrip()

    messages = []
    maxMessage = 0
    while line != "":
        messages.append(line)
        maxMessage = max(maxMessage, len(line))
        line = infile.readline().rstrip()

    return messages, maxMessage

def validateMessages(messages, rule0Strings):
    count = 0
    for message in messages:
        rm = re.match(rule0Strings,message)
        if rm:
            #print(message)
            count += 1
    return count

infile = open(sys.argv[1], "r")

(rules, baseRules) = parseRules(infile)
#print(rules, baseRules)
(messages, maxMessage) = parseMessages(infile)

rule0Strings = expandRule(0, rules, baseRules)
rule0Strings = "^" + rule0Strings + "$"

#print(len(rule0Strings))
print (validateMessages(messages, rule0Strings))
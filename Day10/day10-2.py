#!/bin/python

import sys
import copy
from itertools import combinations

infile = open(sys.argv[1], "r")

input = []

lineNo = 1
for line in infile:
    line = line.rstrip()

    input.append(int(line))

#print input
input.sort()
input.insert(0,0)

maxJolt = input[-1] + 3
input.append(maxJolt)

valid = []
listTails = {}

def validateConfig(config):
    oneJolt = 0
    twoJolt = 0
    threeJolt = 0

    prev = config[0]
    for a in config[1:]:
        #print prev, a
        if a - prev == 1:
            oneJolt += 1
        elif a - prev == 2:
            twoJolt +=1
        elif a - prev == 3:
            threeJolt +=1
        else:
            #print config, "f"
            return False
        prev = a
    #print config, "p"
    return True

    #print "\t", oneJolt, twoJolt, threeJolt

def candidateValues(input, index):
    current = input[index]

    i = index + 1
    while i < len(input):
        if input[i] - current > 3:
            break
        i += 1

    return [(n,a) for (n,a) in zip(range(index+1,i), input[index+1:i])]

def printTails(index):
    print "---"
    for t in listTails[index]:
        print '\t', t
    print "---"

def constructValid(input, index):

    curr = input[index]

    if index == len(input)-1:
        listTails[index] = 1
        return

    for (n,a) in candidateValues(input, index):
        if not listTails.has_key(n):
            constructValid(input,n)

        if not listTails.has_key(index):
            listTails[index] = 0

        listTails[index] += listTails[n]

constructValid(input, 0)

print listTails[0]
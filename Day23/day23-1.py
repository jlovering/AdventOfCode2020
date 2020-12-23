#!/bin/python

import sys
import copy
import re

def parseInput():
    infile = open(sys.argv[1], "r")

    return [int(x) for x in infile.readline().rstrip()]

cups = parseInput()

maxLabel = max(cups)
minLabel = min(cups)

#Keep idx 0 as current

def pickup(cups):
    pickup = []
    pickup.append(cups.pop(1))
    pickup.append(cups.pop(1))
    pickup.append(cups.pop(1))
    return pickup

def findDest(cups, label):
    global maxLabel, minLabel

    tl = label

    while True:
        tl = tl - 1

        #print(tl)
        if tl < minLabel:
            tl = maxLabel

        if tl in cups:
            return cups.index(tl)

def rotateArray(cups, idx):
    shuffle = []

    for _ in range(idx):
        shuffle.append(cups.pop(0))

    cups += shuffle

def putdown(cups, hand, idx):
    cups[idx:idx] = hand

for r in range(100):
    print(r)
    print(cups)
    hand = pickup(cups)
    print(cups)
    print(hand)
    idx = findDest(cups, cups[0])
    print(cups[idx], idx)
    putdown(cups, hand, idx+1)
    rotateArray(cups, 1)
    print("")

idx = findDest(cups, 1)
rotateArray(cups, idx)
print(cups)
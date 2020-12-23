#!/bin/python

import sys
import copy
import re

def parseInput():
    infile = open(sys.argv[1], "r")

    lst = {}
    prev = None
    first = None
    for x in infile.readline().rstrip():
        cur = int(x)
        if prev == None:
            first = cur
            prev = cur
        else:
            lst[prev] = cur
            prev = cur

    return first, prev, lst

first, last, cups = parseInput()
minLabel = min(cups.values())
maxLabel = max(cups.values())

cur = maxLabel + 1
prev = last
for i in range(maxLabel+1, 1000001):
    cur = i
    cups[prev] = cur
    prev = cur

maxLabel = 1000000
cups[prev] = first

#Keep idx 0 as current

def pickup(cups, current):
    pickup = []

    cur = cups[current]
    for _ in range(3):
        pickup.append(cur)
        cur = cups[cur]

    cups[current] = cur

    return pickup

def findDest(label, hand):
    global maxLabel, minLabel

    tl = label - 1
    if tl < minLabel:
        tl = maxLabel

    while tl in hand:
        tl -= 1
        if tl < minLabel:
            tl = maxLabel

    return tl

def putdown(cups, hand, loc):
    prevLink = cups[loc]

    #print(prevLink, loc)
    cur = loc
    cups[cur] = hand[0]
    cur = hand[0]
    cups[cur] = hand[1]
    cur = hand[1]
    cups[cur] = hand[2]
    cur = hand[2]

    cups[cur] = prevLink

def printFakeLinkList(cups, first, limit=10):
    #print(cups)
    print(first, "-> ", end='')
    cur = cups[first]
    i = 0
    while cur != first and i < limit:
        print(cur, "-> ", end='')
        try:
            cur = cups[cur]
        except:
            break
        i += 1

    print("")

def dumpFakeLinkList(cups, first, limit=10):
    #print(cups)
    vals = [first]
    cur = cups[first]
    i = 0
    while cur != first and i < limit:
        vals.append(cur)
        try:
            cur = cups[cur]
        except:
            break
        i += 1

    return vals

current = first
for r in range(1, 10000001):
    if r % 1000000 == 0:
        print("-- move %d current %d--\ncups:" % (r, current))
        printFakeLinkList(cups, current)

    hand = pickup(cups, current)

    dest = findDest(current, hand)


    putdown(cups, hand, dest)

    current = cups[current]

printFakeLinkList(cups, cups[1])
outList = dumpFakeLinkList(cups, cups[1])
print(outList[0]*outList[1])
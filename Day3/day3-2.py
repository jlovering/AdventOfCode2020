#!/bin/python

import sys
import math

map = []

infile = open(sys.argv[1], "r")

for line in infile:
    map.append(list(line.rstrip()))

width = len(map[0])
height = len(map)

print (width)
print (height)

move = (3,1)



results = []

for move in [(1,1), (3,1), (5,1), (7,1), (1,2)]:
    print (move)
    xpos = 0
    ypos = 0

    tree = 0
    clear = 0
    while ypos < height:
        print ("\t\t", xpos, ypos)
        if map[ypos][xpos] == '#':
            tree += 1
        else:
            clear += 1

        ypos += move[1]
        xpos = (xpos + move[0]) % width

    print ("\t", tree, clear)

    results.append(tree)

print (math.prod(results))
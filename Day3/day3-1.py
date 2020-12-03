#!/bin/python

import sys

map = []

infile = open(sys.argv[1], "r")

for line in infile:
    map.append(list(line.rstrip()))

width = len(map[0])
height = len(map)

print width
print height

move = (3,1)

xpos = 0
ypos = 0

tree = 0
clear = 0

while ypos < height/move[1]:
    if map[ypos][xpos] == '#':
        tree += 1
    else:
        clear += 1

    ypos += move[1]
    xpos = (xpos + move[0]) % width

    print (xpos, ypos)

print tree, clear
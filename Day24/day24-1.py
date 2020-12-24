#!/bin/python

import sys
import copy
import re

def parseInput():
    infile = open(sys.argv[1], "r")

    directions = []
    for l in infile:
        dirs = []
        holder = None
        for c in l:
            if holder == None and (c == 'e' or c == 'w'):
                dirs.append(c)
            else:
                if holder is not None:
                    tmp = holder+c
                    dirs.append(tmp)
                    holder = None
                else:
                    holder = c
        directions.append(dirs)

    return directions

directions = parseInput()

print(directions)

# Cube style hex coordinates https://www.redblobgames.com/grids/hexagons/
VECTORS = {
    'ne': (1,-1,0),
    'e': (1,0,-1),
    'se' : (0,1,-1),
    'sw' : (-1,1,0),
    'w' : (-1,0,1),
    'nw' : (0,-1,1)
}

tiles = {}

def followToTile(dirs):
    possition = [0,0,0]
    for d in dirs:
        move = VECTORS[d]
        possition[0] += move[0]
        possition[1] += move[1]
        possition[2] += move[2]

    return tuple(possition)

for d in directions:
    pos = followToTile(d)
    if pos not in tiles:
        tiles[pos] = True
    else:
        tiles[pos] = not tiles[pos]

#print(tiles)
blackTiles = [pos for pos in tiles if tiles[pos]]

print(len(blackTiles))
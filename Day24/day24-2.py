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

#print(directions)

# Cube style hex coordinates https://www.redblobgames.com/grids/hexagons/
VECTORS = {
    'ne': (1,-1,0),
    'e': (1,0,-1),
    'se' : (0,1,-1),
    'sw' : (-1,1,0),
    'w' : (-1,0,1),
    'nw' : (0,-1,1)
}

def followToTile(dirs):
    possition = [0,0,0]
    for d in dirs:
        move = VECTORS[d]
        possition[0] += move[0]
        possition[1] += move[1]
        possition[2] += move[2]

    return tuple(possition)

def initGrid(tiles, d):
    for d in directions:
        pos = followToTile(d)
        if pos not in tiles:
            tiles[pos] = True
        else:
            tiles[pos] = not tiles[pos]

def genPos(pos, dir):
    npos = list(pos)
    npos[0] += dir[0]
    npos[1] += dir[1]
    npos[2] += dir[2]

    return tuple(npos)

def checkDir(tiles, pos, dir):
    npos = genPos(pos,dir)
    if npos in tiles:
        return tiles[npos]
    else:
        return False

def mutateTile(tiles, newDay, pos):
    dirGrid = [ checkDir(tiles, pos, v) for v in VECTORS.values() ]
    blackAdj = len([x for x in dirGrid if x])

    #print(pos, tiles[pos], dirGrid, blackAdj)
    if tiles[pos] == True:
        if blackAdj == 0 or blackAdj > 2:
            #print("\tflip")
            newDay[pos] = False
    else:
        if blackAdj == 2:
            #print("\tflip")
            newDay[pos] = True

def generateNextDay(tiles):
    newDay = copy.copy(tiles)

    for pos in [ x for x in tiles if tiles[x]]:
        for npos in [genPos(pos, v) for v in VECTORS.values()]:
            if npos not in tiles:
                tiles[npos] = False

    for pos in tiles:
        mutateTile(tiles, newDay, pos)

    return newDay

directions = parseInput()

tiles = {}
initGrid(tiles, directions)

for i in range(100):
    #print(tiles)
    tiles = generateNextDay(tiles)
    blackTiles = [ p for p in tiles if tiles[p] ]
    if i % 10 == 0:
        print("Day %d: %d" % ((i+1), len(blackTiles)))

print("Day %d: %d" % ((i+1), len(blackTiles)))

#!/bin/python

import sys
import copy
import re

infile = open(sys.argv[1], "r")

class Cube:
    KEEPALIVECOUNT = [2,3]
    ACTIVATECOUNT = 3

    def __init__(self, active=False):
        self.active = active
        self.nextState = None

    def getState(self):
        return self.active

    def computeCycle(self, neighbours):
        neighbourActiveCount = 0
        for p in neighbours:
            if p.getState():
                neighbourActiveCount += 1

        if self.active:
            if neighbourActiveCount in self.KEEPALIVECOUNT:
                self.nextState = True
            else:
                self.nextState = False
        else:
            if neighbourActiveCount == self.ACTIVATECOUNT:
                self.nextState = True
            else:
                self.nextState = False

        #if self.nextState:
        #    print ("\t On")
        #else:
        #    print ("\t Off")

    def executeCycle(self):
        self.active = self.nextState

    def __str__(self):
        if self.active:
            return "#"
        else:
            return "."

neighbourGrid = [(x,y,z) for x in range(-1,2) for y in range(-1,2) for z in range(-1,2)]
neighbourGrid.remove((0,0,0))

pocketDimension = {}

x = 0
pocketDimension['xmin'] = 0
pocketDimension['ymin'] = 0
pocketDimension['zmin'] = 0
for line in infile:
    line = line.rstrip()

    for (y, c) in enumerate(line):
        #print(y,c)
        pocketDimension['ymax'] = y
        if c == '.':
            pocketDimension[(x,y,0)] = Cube(False)
        elif c == '#':
            pocketDimension[(x,y,0)] = Cube(True)
        else:
            raise Exception("Bad Parse")

    x+=1
pocketDimension['xmax'] = x-1
pocketDimension['zmax'] = 0

def printGrid():
    global pocketDimension
    for z in range(pocketDimension['zmin'], pocketDimension['zmax']+1):
        print("z=%d" % z)
        for x in range(pocketDimension['xmin'], pocketDimension['xmax']+1):
            row = ""
            for y in range(pocketDimension['ymin'], pocketDimension['ymax']+1):
                row += str(pocketDimension[(x,y,z)])
            print(row)

def processGridNode(grid, node, coords, extend=True):
    gridExtend = {}
    if isinstance(node, Cube):
        (x,y,z) = coords
        neighbours = []
        #print(coords)
        for p in neighbourGrid:
            (xoff, yoff, zoff) = p
            if (x+xoff, y+yoff, z+zoff) in grid:
                neighbours.append(grid[(x+xoff, y+yoff, z+zoff)])
            elif extend:
                gridExtend[(x+xoff, y+yoff, z+zoff)] = Cube(False)
                grid['xmin'] = min(grid['xmin'], x+xoff)
                grid['xmax'] = max(grid['xmax'], x+xoff)
                grid['ymin'] = min(grid['ymin'], y+xoff)
                grid['ymax'] = max(grid['ymax'], y+xoff)
                grid['zmin'] = min(grid['zmin'], z+xoff)
                grid['zmax'] = max(grid['zmax'], z+xoff)
                continue
            else:
                continue

        grid[coords].computeCycle(neighbours)

    return gridExtend

def processGrid(grid):
    gridExtend = {}
    for (coords, node) in zip(grid.keys(), grid.values()):
        gridExtend.update(processGridNode(grid, node, coords))

    grid.update(gridExtend)
    for (coords, node) in zip(gridExtend.keys(), gridExtend.values()):
        processGridNode(grid, node, coords, False)


for cycle in range(6):
    print(cycle)
    #printGrid()

    processGrid(pocketDimension)

    for coords in pocketDimension:
        if isinstance(pocketDimension[coords], Cube):
            pocketDimension[coords].executeCycle()

printGrid()

print(sum([ x.getState() for x in pocketDimension.values() if isinstance(x, Cube)]))
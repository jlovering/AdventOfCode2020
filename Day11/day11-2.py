#!/bin/python

import sys
import copy

infile = open(sys.argv[1], "r")

roomMap = []

for line in infile:
    line = line.rstrip()

    roomMap.append([ c for c in line ])

def print_room(rmap):
    for l in rmap:
        for c in l:
            print("%s" % c, end='')
        print("")
    print("===")

def processSeat(rmap, xloc, yloc):
    checkMap = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1),
    ]

    neighboursOccupied = 0

    #print(xloc, yloc, len(roomMap[0]), len(roomMap))
    if rmap[yloc][xloc] == '.':
        return '.'

    for (xcheck, ycheck) in checkMap:
        if (xloc+xcheck < 0 or
            xloc+xcheck > len(rmap[0]) - 1 or
            yloc+ycheck < 0 or
            yloc+ycheck > len(rmap) - 1):
            continue

        if rmap[yloc+ycheck][xloc+xcheck] == '.':
            nxcheck = 0
            nycheck = 0

            if xcheck != 0:
                if xcheck < 0:
                    nxcheck = xcheck-1
                else:
                    nxcheck = xcheck+1
            if ycheck != 0:
                if ycheck < 0:
                    nycheck = ycheck-1
                else:
                    nycheck = ycheck+1

            checkMap.append((nxcheck,nycheck))
            continue

        if rmap[yloc+ycheck][xloc+xcheck] == '#':
            neighboursOccupied += 1

    #print(xloc, yloc, neighboursOccupied, rmap[yloc][xloc])

    if rmap[yloc][xloc] == 'L' and neighboursOccupied == 0:
        return '#'
    elif rmap[yloc][xloc] == '#' and neighboursOccupied >= 5:
        return 'L'
    else:
        return rmap[yloc][xloc]

def processRound():
    global roomMap
    newMap = copy.deepcopy(roomMap)
    for y in range(len(newMap)):
        for x in range(len(newMap[0])):
            newMap[y][x] = processSeat(roomMap, x, y)

    if newMap != roomMap:
        roomMap = newMap
        return True
    else:
        return False

def countEmptySeats():
    emptySeats = 0

    for y in roomMap:
        for x in y:
            if x == 'L':
                emptySeats += 1
    return emptySeats

def countOccSeats():
    occSeats = 0

    for y in roomMap:
        for x in y:
            if x == '#':
                occSeats += 1
    return occSeats

rounds = 1
while processRound():
    #print(rounds)
    #print_room(roomMap)
    #if rounds > 5:
    #    sys.exit()
    rounds += 1
    continue


print_room(roomMap)
print(countEmptySeats())
print(countOccSeats())
#!/bin/python

import sys
import copy
import re
import math

infile = open(sys.argv[1], "r")

dim = 0

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def imageRotateAndFlip(newImage, rotation, flip):
        for _ in range(rotation):
            newImage = [''.join(map(str,list(t))) for t in zip(*[o[::-1] for o in newImage])]

        if flip == 1:
            newerImage = []
            for r in newImage:
                newerImage.append(r[::-1])
            newImage = newerImage
        elif flip == 2:
            newImage = [''.join(map(str,list(t))) for t in zip(*newImage[::-1])]
            newerImage = []
            for r in newImage:
                newerImage.append(r[::-1])
            newImage = newerImage
            newImage = [''.join(map(str,list(t))) for t in zip(*[o[::-1] for o in newImage])]

        return newImage

class Tile:
    def __init__(self, name, data):
        self.name = name

        self.data = data

        self.north = data[0]
        self.south = data[-1]
        self.east = ""
        self.west = ""

        for r in data:
            self.west += r[0]
            self.east += r[-1]

        #print(self.west, self.east)

    def extractImage(self, rotation, flip):
        newImage = [ r[1:-1] for r in self.data[1:-1] ]

        return imageRotateAndFlip(newImage, rotation, flip)

    def rotateEdges(self, edges, rotation):
        north, east, south, west = edges

        if rotation == 0:
            return edges
        elif rotation == 1:
            return [east, south[::-1], west, north[::-1]]
        elif rotation == 2:
            return [south[::-1], west[::-1], north[::-1], east[::-1]]
        elif rotation == 3:
            return [west[::-1], north, east[::-1], south]

    def flipEdges(self, edges, flip):
        north, east, south, west = edges

        if flip == 0:
            return edges
        elif flip == 1:
            return [north[::-1], west, south[::-1], east]
        elif flip == 2:
            return [south, east[::-1], north, west[::-1]]

    def getAllEdges(self, rotation=0, flip=0):
        # Rotations:
        # 0: as found
        # 1: 90d counter clockwise
        # 2: 180d counter clockwise
        # 3: 270d counter clockwise
        # Flip (after rotation:
        # 0: as found
        # 1: horrizontal
        # 2: vertical

        if rotation == 0 and flip == 0:
            return [self.north, self.east, self.south, self.west]

        return self.flipEdges(self.rotateEdges([self.north, self.east, self.south, self.west], rotation), flip)

    def findEdge(self, cand, whichEdge):
        # side:
        # 0 - north
        # 1 - east
        # 2 - south
        # 3 - west
        if cand not in self.getAllEdges() and cand[::-1] not in self.getAllEdges():
            return (False, None, None)

        for rotation in [0, 1, 2, 3]:
            for flip in [0, 1, 2]:
                if cand == self.getAllEdges(rotation, flip)[whichEdge]:
                    return (True, rotation, flip)

def parseInput(infile):
    line = infile.readline().rstrip()

    allTiles = []
    while line != "":
        lineM = re.match(r"Tile (\d+):", line)
        if not lineM:
            raise Exception("")

        data = []
        line = infile.readline().rstrip()
        while line != "":
            data.append(line)
            line = infile.readline().rstrip()

        t = Tile(int(lineM.group(1)), data)

        allTiles.append(t)

        line = infile.readline().rstrip()

    return allTiles

allTiles = parseInput(infile)

def printEdges(edges):
    north, east, south, west = edges
    print(north)
    for i in range(1,len(east)-1):
        print("%s%s%s" % (west[i],'.'*(len(north)-2),east[i]))
    print(south)

def printGrid(grid):
    for row in grid:
        for v in row:
            if v is not None:
                tile, r, f = v
                print(tile.name, r, f, "\t", end='')
            else:
                print("NA\t", end='')
        print("")

def pullEdgeFromGrid(side, grid, x, y):
    # side:
    # 0 - north
    # 1 - east
    # 2 - south
    # 3 - west

    tile, r, f = grid[y][x]
    edges = tile.getAllEdges(r, f)
    return edges[side]

def getNextCoords(x, y):
    global dim

    if x == dim-1:
        return (0, y+1)
    else:
        return (x+1, y)

def gridSolve(grid, remainingTiles, x, y):
    grid = copy.copy(grid)
    remainingTiles = copy.copy(remainingTiles)
    if len(remainingTiles) == 0:
        return grid

    #print("")
    #print(x,y)
    #printGrid(grid)
    #print([rt.name for rt in remainingTiles])

    nx, ny = getNextCoords(x,y)
    if x > 0 and y > 0:
        existingVEdge = pullEdgeFromGrid(EAST, grid, x-1, y)
        existingHEdge = pullEdgeFromGrid(SOUTH, grid, x, y-1)
        for rt in remainingTiles:
            (retv, rv, fv) = rt.findEdge(existingVEdge, WEST)
            #print(existingVEdge, rt.name, retv, rv, fv)
            if retv:
                (reth, rh, fh) = rt.findEdge(existingHEdge, NORTH)
                #print(existingHEdge, rt.name, reth, rh, fh)
                if reth:
                    if rv == rh and fv == fh:
                        remainingTiles.remove(rt)
                        grid[y][x] = (rt, rv, fv)
                        solved = gridSolve(grid, remainingTiles, nx, ny)
                        if solved is not None:
                            return solved
                        grid[y][x] = None
        return None
    elif x > 0:
        existingVEdge = pullEdgeFromGrid(EAST, grid, x-1, y)
        for rt in remainingTiles:
            (retv, rv, fv) = rt.findEdge(existingVEdge, WEST)
            #print(existingVEdge, rt.name, retv, rv, fv)
            if retv:
                remainingTiles.remove(rt)
                grid[y][x] = (rt, rv, fv)
                solved = gridSolve(grid, remainingTiles, nx, ny)
                if solved is not None:
                    return solved
                grid[y][x] = None
        return None
    elif y > 0:
        existingHEdge = pullEdgeFromGrid(SOUTH, grid, x, y-1)
        for rt in remainingTiles:
            (reth, rh, fh) = rt.findEdge(existingHEdge, NORTH)
            #print(existingHEdge, rt.name, reth, rh, fh)
            if reth:
                #printEdges(rt.getAllEdges(rh,fh))
                remainingTiles.remove(rt)
                grid[y][x] = (rt, rh, fh)
                solved = gridSolve(grid, remainingTiles, nx, ny)
                if solved is not None:
                    return solved
                grid[y][x] = None
        return None


def initSolver(allTiles):
    global dim
    #Start in the top left, place a tile, then try to complete the grid

    dim = int(math.sqrt(len(allTiles)))

    grid = [[None for _ in range(dim)] for _ in range(dim)]

    for rt in allTiles:
        remainingTiles = copy.copy(allTiles)
        remainingTiles.remove(rt)
        for rotation in [0,1,2,3]:
            for flip in [0,1,2]:
        #for rotation in [0]:
        #    for flip in [2]:
                grid[0][0] = (rt, rotation, flip)
                solved = gridSolve(grid, remainingTiles, 1, 0)
                if solved is not None:
                    return solved

def constructBigPicture(solution):
    bigPicture = [ "" for _ in range(dim*(len(solution[0][0][0].data)-2)) ]
    j = 0
    for row in solution:
        for (tile, r, f) in row:
            for (i, imgr) in enumerate(tile.extractImage(r,f)):
                bigPicture[i+j] += imgr
                bigPicture[i+j] += ""
        j += i + 1

    return bigPicture

def findMonsters(picture):
    monsterl1 = re.compile(r".{18}#.{1}.*")
    monsterl2 = re.compile(r"#.{4}##.{4}##.{4}###.*")
    monsterl3 = re.compile(r".{1}#.{2}#.{2}#.{2}#.{2}#.{2}#.*")

    monstersFound = 0

    for i in range(len(picture)-2):
        #print (picture[i])
        for offset in range(len(picture[i]) - 19):
            monsterl1M = monsterl1.match(picture[i][offset:])
            monsterl2M = monsterl2.match(picture[i+1][offset:])
            monsterl3M = monsterl3.match(picture[i+2][offset:])
            #print(offset, monsterl1M, monsterl2M, monsterl3M)
            if monsterl1M is not None:
                #print(i, "l1")
                if monsterl2M is not None:
                    #print("l2")
                    if monsterl3M is not None:
                        #print("l3")
                        monstersFound += 1
        #print("")

    return monstersFound

def countWaves(picture):
    count = 0
    for r in picture:
        count += r.count('#')

    return count

solution = initSolver(allTiles)
printGrid(solution)

bigPicture = constructBigPicture(solution)

#bigPicture = [
#".####...#####..#...###..",
#"#####..#..#.#.####..#.#.",
#".#.#...#.###...#.##.##..",
#"#.#.##.###.#.##.##.#####",
#"..##.###.####..#.####.##",
#"...#.#..##.##...#..#..##",
#"#.##.#..#.#..#..##.#.#..",
#".###.##.....#...###.#...",
#"#.####.#.#....##.#..#.#.",
#"##...#..#....#..#...####",
#"..#.##...###..#.#####..#",
#"....#.##.#.#####....#...",
#"..##.##.###.....#.##..#.",
#"#...#...###..####....##.",
#".#.##...#.##.#.#.###...#",
#"#.###.#..####...##..#...",
#"#.###...#.##...#.######.",
#".###.###.#######..#####.",
#"..##.#..#..#.#######.###",
#"#.#..##.########..#..##.",
#"#.#####..#.#...##..#....",
#"#....##..#.#########..##",
#"#...#.....#..##...###.##",
#"#..###....##.#...##.##.#",
#]

for r in bigPicture:
    print(r)
print("")

for r in [0,1,2,3]:
    for f in [0,1,2]:
        monsterCount = findMonsters(imageRotateAndFlip(bigPicture, r, f))
        if monsterCount > 0:
            waveCount = countWaves(imageRotateAndFlip(bigPicture, r, f))
            waveCount -= 15 * monsterCount
            print(monsterCount, waveCount)


#for r in solution[0][0][0].data:
#    print(r)
#print("")
#
#for rot in [1, 2, 3]:
#    for f in [0, 1, 2]:
#        print(rot, f)
#        outImage = solution[0][0][0].extractImage(rot, f)
#        for r in outImage:
#            print(r)
#        print("")

#print(solution[0][0][0].name * solution[0][dim-1][0].name * solution[dim-1][0][0].name * solution[dim-1][dim-1][0].name)

#n, e, s, w = allTiles[0].getAllEdges(0,0)
#
#for t in allTiles[1:]:
#    print(t.name)
#    (found, r, f) = t.findEdge(e)
#    if found:
#        print(t.name, r, f)

#print("You spin me right round")
#printEdges(allTiles[0].getAllEdges(0,0))
#print("")
#printEdges(allTiles[0].getAllEdges(1,0))
#print("")
#printEdges(allTiles[0].getAllEdges(2,0))
#print("")
#printEdges(allTiles[0].getAllEdges(3,0))
#print("")
#print("Flip that bitch")
#printEdges(allTiles[0].getAllEdges(0,1))
#print("")
#printEdges(allTiles[0].getAllEdges(0,2))
#print("")
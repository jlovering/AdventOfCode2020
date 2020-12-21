#!/bin/python

import sys
import copy
import re

infile = open(sys.argv[1], "r")

allergenSetMap = {}
#allIngredients = {}

for line in infile:
    line = line.rstrip()

    lineM = re.match(r"^(.*) \(contains (.*)\)$", line)
    if not lineM:
        raise Exception("Line didn't parse")

    ingredientList = lineM.group(1).split(" ")
    allergenList = lineM.group(2).split(", ")

    for a in allergenList:
        if a in allergenSetMap:
            allergenSetMap[a] = allergenSetMap[a].intersection(set(ingredientList))
        else:
            allergenSetMap[a] = set(ingredientList)


def cullList(allergenSetMap, k, s):
    for v in s:
        for ka, aS in allergenSetMap.items():
            #print("\t", ka, aS, ka != k, v in aS)
            if ka != k and v in aS:
                #print("2")
                aS.remove(v)
                if len(aS) == 1:
                    cullList(allergenSetMap, ka, aS)

for k, s in allergenSetMap.items():
    if len(s) == 1:
        cullList(allergenSetMap, k, s)

#print(allergenSetMap)

dangerousAllergens = sorted([ x for x in allergenSetMap.keys()])

#print(dangerousAllergens)

print(','.join([list(allergenSetMap[a])[0] for a in dangerousAllergens]))
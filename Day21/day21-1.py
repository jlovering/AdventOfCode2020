#!/bin/python

import sys
import copy
import re

infile = open(sys.argv[1], "r")

allergenSetMap = {}
allIngredients = {}

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

    for i in ingredientList:
        if i in allIngredients:
            allIngredients[i] += 1
        else:
            allIngredients[i] = 1

print(allergenSetMap)

allPotentialAllergens = set()
for a in allergenSetMap.values():
    allPotentialAllergens = allPotentialAllergens.union(a)

print(allPotentialAllergens)

for a in allPotentialAllergens:
    if a in allIngredients:
        allIngredients.pop(a, None)

print(sum([x for x in allIngredients.values()]))
#!/bin/python

import sys

def validate(passport):
    fields = [
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
        #"cid"
        ]

    print passport, len(passport)
    if len(passport) < 7:
        return 0
    for field in fields:
        print field, passport.has_key(field)
        if not passport.has_key(field):
            return 0
    return 1

infile = open(sys.argv[1], "r")

current = {}
valid = 0

for line in infile:
    if line == "\n":
        valid += validate(current)
        current = {}
    pairs = line.rstrip().split(" ")
    for p in pairs:
        if p == "":
            break
        pp = p.split(":")
        current[pp[0]] = pp[1]

print valid
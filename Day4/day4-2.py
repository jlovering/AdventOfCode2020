#!/bin/python

import sys
import re

def valid_byr(value):
    year = re.search(r"\d{4}", value)
    if year is None:
        return False
    return (int(year.group()) >= 1920 and int(year.group()) <= 2002)

def valid_iyr(value):
    year = re.search(r"\d{4}", value)
    if year is None:
        return False
    return (int(year.group()) >= 2010 and int(year.group()) <= 2020)

def valid_eyr(value):
    year = re.search(r"\d{4}", value)
    if year is None:
        return False
    return (int(year.group()) >= 2020 and int(year.group()) <= 2030)

def valid_hgt(value):
    hgt = re.search(r"(\d+)(cm|in)", value)
    if hgt is None:
        return False
    #print hgt, hgt.group(1), hgt.group(2)
    if hgt.group(2) == 'cm':
        return (int(hgt.group(1)) >= 150 and int(hgt.group(1)) <= 193)
    if hgt.group(2) == 'in':
        return (int(hgt.group(1)) >= 59 and int(hgt.group(1)) <= 76)
    return False


def valid_hcl(value):
    hcl = re.search(r"^#[0-9a-f]{6}$", value)
    if hcl is None:
        return False
    return True

def valid_ecl(value):
    return value in [
        'amb',
        'blu',
        'brn',
        'gry',
        'grn',
        'hzl',
        'oth']

def valid_pid(value):
    pid = re.search(r"^[0-9]{9}$", value)
    if pid is None:
        return False
    return True

def validate(passport):
    fields = {
        "byr" : valid_byr,
        "iyr" : valid_iyr,
        "eyr" : valid_eyr,
        "hgt" : valid_hgt,
        "hcl" : valid_hcl,
        "ecl" : valid_ecl,
        "pid" : valid_pid
        }

    if len(passport) < 7:
        return 0
    for field in fields.keys():
        if not passport.has_key(field):
            print "badf", passport, field
            return 0
        if not fields[field](passport[field]):
            print "badv", passport, field, passport[field]
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
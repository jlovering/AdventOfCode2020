#!/bin/python

import sys
import copy
import re

def twoPlaceEval(t1, op, t2):
    ret = 0
    if op == '+':
        ret = t1 + t2
    elif op == '*':
        ret = t1 * t2
    else:
        raise Exception("Bad Operator")

    return ret

class Expression():
    def __init__(self, terms):
        self.terms = terms

    def __str__(self):
        return str(self.terms)

    def evaluate(self):
        evalSoFar = self.terms[0]
        if isinstance(evalSoFar, Expression):
            evalSoFar = evalSoFar.evaluate()
        else:
            evalSoFar = int(evalSoFar)

        op, term, *remaining = self.terms[1:]

        if isinstance(term, Expression):
            term = term.evaluate()
        else:
            term = int(term)

        while len(remaining) > 0:
            #print(evalSoFar, op, term, remaining)
            evalSoFar = twoPlaceEval(evalSoFar, op, term)

            op, term, *remaining = remaining

            if isinstance(term, Expression):
                term = term.evaluate()
            else:
                term = int(term)

        return twoPlaceEval(evalSoFar, op, term)

def parseLine(line):
    line = line.replace(' ', '')
    stack = []
    for c in line:
        if c == ')':
            terms = []
            t = stack.pop()
            while t != '(':
                terms.insert(0, t)
                t = stack.pop()
            #print("\t", terms)
            stack.append(Expression(terms))
            #print(stack)
            continue
        stack.append(c)
        #print(stack)

    return Expression(stack)

def parseInput():
    infile = open(sys.argv[1], "r")

    equations = []
    for line in infile:
        #print(line)
        equations.append(parseLine(line.rstrip()))

    return equations

equations = parseInput()

#for e in equations:
#    print(e)
#    print(e.evaluate())

print(sum([e.evaluate() for e in equations]))

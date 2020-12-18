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
        #print(terms)
        self.terms = terms

    def __str__(self):
        return str(self.terms)

    def evaluate(self):
        if len(self.terms) == 1:
            if isinstance(self.terms[0], Expression):
                 return self.terms[0].evaluate()
            else:
                return int(self.terms[0])

        evalSoFar = self.terms[0]
        if isinstance(evalSoFar, Expression):
            evalSoFar = evalSoFar.evaluate()
        else:
            evalSoFar = int(evalSoFar)

        #print("\t", self.terms)
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

def expresionize(terms):
    t1, op, t2, *remaining = terms

    outterms = []
    while len(remaining) > 0:
        if op == '+':
            t1 = Expression([t1,op,t2])
        else:
            outterms += [t1, op]
            t1 = t2
        op, t2, *remaining = remaining

    if op == '+':
            outterms.append(Expression([t1,op,t2]))
    else:
        outterms += [t1, op, t2]

    return outterms

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
            if len(terms) > 3:
                stack.append(Expression(expresionize(terms)))
            else:
                stack.append(Expression(terms))
            #print(stack)
            continue
        stack.append(c)
        #print(stack)

    return Expression(expresionize(stack))

def parseInput():
    infile = open(sys.argv[1], "r")

    equations = []
    for line in infile:
        #print("\n", line)
        equations.append(parseLine(line.rstrip()))

    return equations

equations = parseInput()

#for e in equations:
#    print(e)
#    print(e.evaluate())
#    print()

print(sum([e.evaluate() for e in equations]))

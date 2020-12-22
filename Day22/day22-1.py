#!/bin/python

import sys
import copy
import re

infile = open(sys.argv[1], "r")

class Deck:
    def __init__(self, player, cards):
        self.name = player
        self.cards = cards

    def drawCard(self):
        return self.cards.pop(0)

    def winRound(self, cards):
        self.cards += cards

    def cardCount(self):
        return len(self.cards)

    def outaCards(self):
        return self.cardCount() == 0

    def computeScore(self):
        score = 0
        for (i, c) in enumerate(self.cards[::-1]):
            #print(i+1,c)
            score += (i+1)*c
        return score

    def __str__(self):
        return "%s " % self.name + str(self.cards)

def processInput(infile):
    players = []
    for _ in range(2):
        line = infile.readline().rstrip()

        name = line.split(':')[0]

        cards = []

        line = infile.readline().rstrip()
        while line != "":
            cards.append(int(line))
            line = infile.readline().rstrip()

        players.append(Deck(name, cards))

    return players

players = processInput(infile)

won = False
i = 1
while not won:
    table = []
    print("-- Round %d --" % i)
    print(players[0])
    print(players[1])
    table.append(players[0].drawCard())
    table.append(players[1].drawCard())

    print(table)

    if table[0] > table[1]:
        print("Player 1 won: ", table)
        players[0].winRound(table)
    else:
        print("Player 2 won: ", table)
        players[1].winRound(table[::-1])

    if any(p.outaCards() for p in players):
        won = True

    print("")
    i += 1

print(players[0])
print(players[1])

for p in players:
    print(p.computeScore())
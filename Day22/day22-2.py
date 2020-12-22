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

    def recurse(self, depth):
        return Deck(self.name, self.cards[:depth])

    def __str__(self):
        return "%s " % self.name + str(self.cards)

gameID = 2
class Game:
    def __init__(self, player1, player2, gameID):
        self.previousRounds = set()
        self.p1 = player1
        self.p2 = player2
        self.gameID = gameID

    def play(self):
        global gameID
        won = False
        i = 1

        #print("\n-- Game %d --" % (self.gameID))
        winArray = [False, False]
        while not any(winArray):
            #print("-- Game %d, Round %d --" % (self.gameID, i))
            #print(self.p1)
            #print(self.p2)

            if tuple(self.p1.cards + ['|'] + self.p2.cards) in self.previousRounds:
                #print ("Recursion Break")
                #print(self.previousRounds)
                winArray = [True, False]
                break

            if tuple(self.p1.cards + ['|'] + self.p2.cards) not in self.previousRounds:
                self.previousRounds.add(tuple(self.p1.cards + ['|'] + self.p2.cards))
                #print(self.previousRounds)

            p1Card = self.p1.drawCard()
            p2Card = self.p2.drawCard()

            winner = None
            if self.p1.cardCount() >= p1Card and self.p2.cardCount() >= p2Card:
                newGame = Game(self.p1.recurse(p1Card), self.p2.recurse(p2Card), gameID)
                gameID += 1
                winner = newGame.play()


            if winner is None:
                if p1Card > p2Card:
                    winner = 1
                else:
                    winner = 2

            if winner == 1:
                #print("Player 1 won: ", [p1Card, p2Card])
                self.p1.winRound([p1Card, p2Card])
            else:
                #print("Player 2 won: ", [p1Card, p2Card])
                self.p2.winRound([p2Card, p1Card])

            winArray = [self.p2.outaCards(), self.p1.outaCards()] #This is not a mistake
            #print("")
            i += 1

        for i, p in enumerate(winArray):
            #print(i,p)
            if p:
                return i+1

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

winner = Game(players[0], players[1], 1).play()

print(str(players[winner-1]), players[winner-1].computeScore())
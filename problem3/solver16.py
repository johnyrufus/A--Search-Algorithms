#!/usr/bin/env python
"""
Authors: Chris Falter, Johny Rufus John, and Xing Liu
Solves the 15-tile problem
Board is represented as a numpy ndarray with elements in set {0 - 15}
The zero is the empty square, elements 1 - 15 represent the tiles
The goal state is:
 1  2  3  4
 5  6  7  8
 9 10 11 12
13 14 15 --
"""

import numpy as np

class Node():
    
    def __init__(self, prevNode, numPrevMoves, state, move, estimatedDistanceToGoal):
        self.prevNode = prevNode
        self.numPrevMoves = numPrevMoves
        self.state = state
        self.move = move
        self.estimatedDistanceToGoal = estimatedDistanceToGoal        

def findEmptySquare(puzzle):
    '''
    puzzle = ndarray(4,4) with elements in range(15)
    returns tuple indicating (row, column) where the zero element is located
    '''
    locationZero = np.where(0 == puzzle)
    return (locationZero[0][0], locationZero[1][0])

def getEstimatedDistanceToGoal(puzzle):
    '''
    puzzle = ndarray(4,4) with elements in range(15)
    heuristic function for estimating distance to goal state
    '''
    pass
    
def isSolvable(puzzle):
    '''
    puzzle = ndarray(4,4) with elements in range(15)
    puzzle is solvable iff sum of permutation inversions is even
    '''
    parity = 0
    puzzle = puzzle.reshape(1,16)[0]
    for i in range(15):
        n = puzzle[i]
        if n < 2:
            continue
        for m in range(i+1, 16):
            if puzzle[m] == 0:
                continue
            if puzzle[m] < n:
                parity = parity + 1
                print str(puzzle[m]) + " < " + str(n)
    return (parity % 2 == 0)
            
            
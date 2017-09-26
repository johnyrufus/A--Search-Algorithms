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

# list of goal positions for each tile + empty space
tileGoal = [(3,3),(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2)]
successors = {}

def initSuccessorDict(d):
    '''
    builds a set of 6 possible moves for each square on the 4x4 board
    zero-based indexing used for location, per the python/numpy convention; however, the move encoding is one-based
    '''
    d[(0,0)] = ["U11","U21","U31","L11","L21","L31"]
    d[(0,1)] = ["U12","U22","U32","L11","L21","R11"]
    d[(0,2)] = ["U13","U23","U33","L11","R11","R21"]
    d[(0,3)] = ["U14","U24","U34","R11","R21","R31"]
    d[(1,0)] = ["U11","U21","D11","L12","L22","L32"]
    d[(1,1)] = ["U12","U22","D12","L12","L22","R12"]
    d[(1,2)] = ["U13","U23","D13","L12","R12","R22"]
    d[(1,3)] = ["U14","U24","D14","R12","R22","R32"]
    d[(2,0)] = ["U11","D11","D21","L13","L23","L33"]
    d[(2,1)] = ["U12","D12","D22","L13","L23","R13"]
    d[(2,2)] = ["U13","D13","D23","L13","R13","R23"]
    d[(2,3)] = ["U14","D14","D24","R13","R23","R33"]
    d[(3,0)] = ["D11","D21","D31","L14","L24","L34"]
    d[(3,1)] = ["D12","D22","D32","L14","L24","R14"]
    d[(3,2)] = ["D13","D23","D33","L14","R14","R24"]
    d[(3,3)] = ["D14","D24","D34","R14","R24","R34"]
   
        
def findTile(val, puzzle):
    '''
    puzzle = ndarray(4,4) with elements in range(15)
    returns tuple indicating (row, column) where the tile having val is located
    '''
    location = np.where(val == puzzle)
    return (location[0][0], location[1][0])

def estimateDistance(puzzle):
    '''
    puzzle = ndarray(4,4) with elements in range(15)
    heuristic function for estimating distance to goal state = 
    Sum of Manhattan distance for each tile from its goal position
    '''
    dist = 0
    for i in range(1,16):
        goal = tileGoal[i]
        actual = findTile(i, puzzle)
        dist += (abs(goal[0] - actual[0]) + abs(goal[1] - actual[1]))
    return dist / 3   
    
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
    return (parity % 2 == 0)

def swapTiles(pos1, pos2, puzzle):
    '''
    swap the tiles that are in position 1 and position 2
    '''
    puzzle[pos1], puzzle[pos2] = puzzle[pos2], puzzle[pos1]

def getNewZeroPosition(oldZero, direction):
    newRow = oldZero[0] if direction in ['R','L'] else oldZero[0] - 1 if direction == 'D' else oldZero[0] + 1
    newCol = oldZero[1] if direction in ['D','U'] else oldZero[1] - 1 if direction == 'R' else oldZero[1] + 1
    return tuple([newRow,newCol])
           
def getSuccessors(node):
    '''
    return an unordered list of the 6 successors to the puzzle state passed as arg
    '''
    successors = []
    locationZero = findTile(0, node.state)
    for move in successors[locationZero]:
        newPuzzle = node.state.copy()
        newZero = locationZero
        direction = move[0]
        numTiles = move[1]
        for i in range(numTiles):
            oldZero = newZero
            newZero = getNewZeroPosition(oldZero, direction)
            swapTiles(oldZero, newZero, newPuzzle)
        successor = Node(node, node.numPrevMoves + 1, newPuzzle, move, estimateDistance(newPuzzle))
        successors.append(successor)
    return successors
                
                
                
        
        
            
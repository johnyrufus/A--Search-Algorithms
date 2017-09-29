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
from heapq import heappush, heappop

class Node():
    
    def __init__(self, prevNode, numPrevMoves, state, move):
        self.PrevNode = prevNode
        self.NumPrevMoves = numPrevMoves
        self.State = state
        self.Move = move
        self.EstimatedDistanceToGoal = estimateDistance(state)
        self.Priority = numPrevMoves + self.EstimatedDistanceToGoal
        self.Hash = hashPuzzle(state)
        self.Removed = False

def initSuccessorMap(d):
    '''
    builds a list of 6 possible moves for each empty square on the 4x4 board
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
   
# list of goal positions for each tile + empty space
tileGoal = [(3,3),(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2)]
successorMap = {}
initSuccessorMap(successorMap)

# the built-in hash has 64 bits on 64-bit platforms. There are 16! permutations 
# of the puzzle. Probability of no collisions = ((2^64 - 1)/(2^64))^(16!) = 99.77%
# So we use the built-in hash function 
def hashPuzzle(puzzle):
    '''
    Returns hash of a puzzle state. Converts state to a one-dimensional tuple,
    then hashes the tuple
    '''
    t = tuple(puzzle.reshape(1,16)[0])
    return hash(t)
        
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
    return dist / 3.0   
    
def isSolvable(puzzle):
    '''
    puzzle = ndarray(4,4) with elements in range(15)
    puzzle is solvable iff sum of permutation inversions is equal to parity
    parity is odd if 0-tile is in an odd row (zero-based), even if 0-tile is in an even row
    '''
    parity = (findTile(0, puzzle)[0] + 1) % 2
    inversions = 0
    puzzle = puzzle.reshape(1,16)[0]
    for i in range(15):
        n = puzzle[i]
        if n < 2:
            continue
        for m in range(i+1, 16):
            if puzzle[m] == 0:
                continue
            if puzzle[m] < n:
                inversions = inversions + 1
    return (inversions % 2 == parity)

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
    zeroPosition = findTile(0, node.State)
    for move in successorMap[zeroPosition]:
        newPuzzle = node.State.copy()
        newZero = zeroPosition
        direction = move[0]
        numTiles = int(move[1])
        for i in range(numTiles):
            oldZero = newZero
            newZero = getNewZeroPosition(oldZero, direction)
            swapTiles(oldZero, newZero, newPuzzle)
        successor = Node(node, node.NumPrevMoves + 1, newPuzzle, move)
        successors.append(successor)
    return successors

def getSolutionMoves(node):
    '''
    given the goal node, returns a list of moves from initial state to goal
    '''
    moves = []
    while (node.Move):
        moves.append(node.Move)
        node = node.PrevNode
    return list(reversed(moves))
    

class AStar():

    def __init__(self, initialState):               
        if not isSolvable(initialState):
            raise ValueError("puzzle cannot be solved!")
        self.closed = set()
        self.fringe = []
        self.nodeFinder = {}
        startNode = Node(None, 0, initialState, None)
        self.addToFringe(startNode)
        
    def addToFringe(self, node):
        if node.Hash in self.closed:
            return
        if node.Hash in self.nodeFinder.keys():
            prevNode = self.nodeFinder[node.Hash]
            if prevNode.Priority <= node.Priority:
                return
            # remove the previous node, the new node will take its place
            del self.nodeFinder[node.Hash]
            prevNode.Removed = True
        heappush(self.fringe, [node.Priority, node])
        self.nodeFinder[node.Hash] = node
        
    def popFromFringe(self):
        _, node = heappop(self.fringe)
        if node.Removed:
            return self.popFromFringe()
        del self.nodeFinder[node.Hash]
        self.closed.add(node.Hash)
        return node
    
    def solve(self):
        '''
        Returns a list of the moves from initial state to goal state. Since A*
        search is used, the path is optimal. If no path is found, throws a
        RuntimeError
        '''
        while(len(self.fringe) > 0):
            node = self.popFromFringe()
            if node.EstimatedDistanceToGoal == 0:
                # we found the goal state!
                return getSolutionMoves(node)
            for n in getSuccessors(node):
                self.addToFringe(n)
        raise RuntimeError("Did not find a solution")
        
def main():
    initialState =  np.array([[1,2,3,4],[5,6,7,8],[9,10,15,11],[13,14,0,12]])
    solver = AStar(initialState)
    actual = solver.solve()
    print actual
    
if __name__ == '__main__':
    main()

            
        
            
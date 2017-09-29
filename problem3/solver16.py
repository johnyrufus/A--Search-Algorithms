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
        self.EstimatedMoves = estimateMoves(state)
        self.Priority = numPrevMoves + self.EstimatedMoves
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
# (row, col) = tileGoal[tileNum]
tileGoal = np.array([(3,3),(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2)])
successorMap = {}
initSuccessorMap(successorMap)

# the built-in hash has 64 bits on 64-bit platforms. There are 16! permutations 
# of the puzzle. Probability of collision = 1 - ((2^64 - 1)/(2^64))^(16!/2) = 0.12%
# In practice the probability of collision is even smaller because not all nodes
# are visited. So we use the built-in hash function 
def hashPuzzle(puzzle):
    '''
    Returns hash of a puzzle state. Converts state to a one-dimensional tuple,
    then hashes the tuple
    '''
    return hash(tuple(puzzle.reshape(1,16)[0]))
        
def findTile(val, puzzle):
    '''
    puzzle = ndarray(4,4) with elements in range(15)
    returns tuple indicating (row, column) where the tile having val is located
    '''
    location = np.where(val == puzzle)
    return (location[0][0], location[1][0])

# vectorized functions that return a boolean mask array
fRow0 = np.vectorize(lambda x: x in set([1,2,3,4]))
fRow1 = np.vectorize(lambda x: x in set([5,6,7,8]))
fRow2 = np.vectorize(lambda x: x in set([9,10,11,12]))
fRow3 = np.vectorize(lambda x: x in set([13,14,15]))
fRow = [fRow0, fRow1, fRow2, fRow3]

fCol0 = np.vectorize(lambda x: x in set([1,5,9,13]))
fCol1 = np.vectorize(lambda x: x in set([2,6,10,14]))
fCol2 = np.vectorize(lambda x: x in set([3,7,11,15]))
fCol3 = np.vectorize(lambda x: x in set([4,8,12]))
fCol = [fCol0, fCol1, fCol2, fCol3]

def getLinearConflicts(puzzle):
    numConflicts = 0
    for i in range(4):
        # get conflicts for i-th row and i-th column
        # apply the i-th row mask to the i-th row and the i-th column mask to the i-th column
        inRowElements = puzzle[i][fRow[i](puzzle[i])]
        numConflicts += getLinearConflictsInRank(inRowElements)
        inColElements = puzzle[:,i][fCol[i](puzzle[:,i])]
        numConflicts += getLinearConflictsInRank(inColElements)
    return numConflicts
    

def getLinearConflictsInRank(inRankElements):
    numElements = len(inRankElements)
    if numElements < 2:
        return 0
    numConflicts = 0    
    for i in range(numElements - 1):
        for val in inRankElements[i+1:]:
            numConflicts += (val < inRankElements[i])
    return numConflicts        

def estimateDistance(puzzle):
    distL1 = 0
    for i in range(1,16):
        goal = tileGoal[i]
        actual = findTile(i , puzzle)
        distL1 += (abs(goal[0] - actual[0]) + abs(goal[1] - actual[1]))
    return distL1
    
def estimateMoves(puzzle):
    '''
    puzzle = ndarray(4,4) with elements in range(15)
    heuristic function for estimating distance to goal state = 
    Sum of Manhattan distance for each tile from its goal position + 2 * linear conflicts
    Divided by 3 because of the ability to slide 3 tiles in a single move
    Inspired by https://algorithmsinsight.wordpress.com/graph-theory-2/a-star-in-general/implementing-a-star-to-solve-n-puzzle/
    '''
    distL1 = estimateDistance(puzzle)
    linearConflicts = getLinearConflicts(puzzle)
    return ((distL1 + 2 * linearConflicts) / 3.0)   
    
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
#        self.removed = 0
#        self.ignoredClosed = 0
#        self.ignoredPriority = 0
        
    def addToFringe(self, node):
        if node.Hash in self.closed:
#            self.ignoredClosed += 1
            return
        prevNode = self.nodeFinder.get(node.Hash)
        if prevNode:
            if prevNode.Priority <= node.Priority:
#                self.ignoredPriority += 1
                return
            # remove the previous node, the new node will take its place
            del self.nodeFinder[node.Hash]
            prevNode.Removed = True
        heappush(self.fringe, [node.Priority, node])
        self.nodeFinder[node.Hash] = node
        
    def popFromFringe(self):
        _, node = heappop(self.fringe)
        if node.Removed:
#            self.removed += 1
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
            if node.EstimatedMoves == 0:
                # we found the goal state!
#                print "Number of nodes ignored because already in closed: : " + str(self.ignoredClosed)
#                print "Number of nodes ignored because already in fringe: " + str(self.ignoredPriority)
#                print "Number of nodes removed nodes encountered: " + str(self.removed)
#                print "Number of nodes in closed: " + str(len(self.closed))
#                print "Number of nodes in fringe: " + str(len(self.fringe))
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

            
        
            
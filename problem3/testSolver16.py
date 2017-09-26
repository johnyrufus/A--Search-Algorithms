# -*- coding: utf-8 -*-
"""
Authors: Chris Falter, Johny Rufus John, and Xing Liu
Test the 15-tile puzzle solver code
"""
import unittest
from solver16 import findTile, isSolvable, estimateDistance, hashPuzzle, getSuccessors, Node
import numpy as np

class TestSolver16(unittest.TestCase):
    
    def test_findTile_ReturnsCorrectLocation(self):
        puzzle = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
        argToLocation = {0:(0,0), 1:(0,1), 2:(0,2), 3:(0,3), 5:(1,1), 10:(2,2), 14:(3,2), 15:(3,3)}
        for arg, location in argToLocation.items():
            self.assertEquals(findTile(arg, puzzle), location)
        
    def test_isSolvable_WithUnsolvableState_ReturnsFalse(self):
        puzzle = np.array([[2,1,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
        self.assertFalse(isSolvable(puzzle))
        
    def test_isSolvable_WithSolvableState_ReturnsTrue(self):
        puzzle = np.array([[1,2,3,4],[7,5,6,12],[8,9,10,11],[13,14,15,0]])
        self.assertTrue(isSolvable(puzzle))
        
    def test_estimateDistance_ReturnsTotalManhattanDistance(self):
        puzzle0 = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
        puzzle1 = np.array([[2,1,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
        puzzle2 = np.array([[1,2,3,4],[7,5,6,12],[8,9,10,11],[13,14,15,0]])
        distToPuzzle = {8:puzzle0, (2/3):puzzle1, 4:puzzle2}
        for dist, puzzle in distToPuzzle.items():
            self.assertEquals(estimateDistance(puzzle), dist)        
        
    def test_getSuccessors_withTopLeftCornerEmpty_Returns6Successors(self):
        puzzle = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
        expected = []
        expected.append(np.array([[1,0,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]))
        expected.append(np.array([[1,2,0,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]))
        expected.append(np.array([[1,2,3,0],[4,5,6,7],[8,9,10,11],[12,13,14,15]]))
        expected.append(np.array([[4,1,2,3],[0,5,6,7],[8,9,10,11],[12,13,14,15]]))
        expected.append(np.array([[4,1,2,3],[8,5,6,7],[0,9,10,11],[12,13,14,15]]))
        expected.append(np.array([[4,1,2,3],[8,5,6,7],[12,9,10,11],[0,13,14,15]]))
        self.verifySuccessorsFunction(puzzle, expected)
    
    def test_getSuccessors_withBottomRightCornerEmpty_Returns6Successors(self):
        puzzle = np.array([[3,1,2,4],[5,6,7,8],[9,10,11,12],[15,13,14,0]])
        expected = []
        expected.append(np.array([[3,1,2,4],[5,6,7,8],[9,10,11,12],[15,13,0,14]]))
        expected.append(np.array([[3,1,2,4],[5,6,7,8],[9,10,11,12],[15,0,13,14]]))
        expected.append(np.array([[3,1,2,4],[5,6,7,8],[9,10,11,12],[0,15,13,14]]))
        expected.append(np.array([[3,1,2,4],[5,6,7,8],[9,10,11,0],[15,13,14,12]]))
        expected.append(np.array([[3,1,2,4],[5,6,7,0],[9,10,11,8],[15,13,14,12]]))
        expected.append(np.array([[3,1,2,0],[5,6,7,4],[9,10,11,8],[15,13,14,12]]))        
        self.verifySuccessorsFunction(puzzle, expected)
    
    def test_getSuccessors_withNonEdgeEmpty_Returns6Successors(self):
        puzzle = np.array([[1,2,3,4],[5,0,6,7],[8,9,10,11],[12,13,14,15]])
        expected = []
        expected.append(np.array([[1,2,3,4],[0,5,6,7],[8,9,10,11],[12,13,14,15]]))
        expected.append(np.array([[1,2,3,4],[5,6,0,7],[8,9,10,11],[12,13,14,15]]))
        expected.append(np.array([[1,2,3,4],[5,6,7,0],[8,9,10,11],[12,13,14,15]]))
        expected.append(np.array([[1,0,3,4],[5,2,6,7],[8,9,10,11],[12,13,14,15]]))
        expected.append(np.array([[1,2,3,4],[5,9,6,7],[8,0,10,11],[12,13,14,15]]))
        expected.append(np.array([[1,2,3,4],[5,9,6,7],[8,13,10,11],[12,0,14,15]]))
        self.verifySuccessorsFunction(puzzle, expected)
    
    def verifySuccessorsFunction(self, state, expected):
        '''
        state = puzzle state
        expected = list of expected puzzle states (should have length 6)
        '''
        if len(expected) != 6:
            raise ValueError("Unexpected number of successors (should be 6)")
        hashesExpected = set()
        for p in expected:
            hashesExpected.add(hashPuzzle(p))
        actual = getSuccessors(Node(None, 0, state, None))
        for n in actual:
            self.assertIn(hashPuzzle(n.State), hashesExpected)

if __name__ == '__main__':
    unittest.main()

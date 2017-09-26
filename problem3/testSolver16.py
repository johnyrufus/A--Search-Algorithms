# -*- coding: utf-8 -*-
"""
Authors: Chris Falter, Johny Rufus John, and Xing Liu
Test the 15-tile puzzle solver code
"""
import unittest
from solver16 import findTile, isSolvable, estimateDistance
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
        

if __name__ == '__main__':
    unittest.main()

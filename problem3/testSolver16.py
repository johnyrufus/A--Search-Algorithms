# -*- coding: utf-8 -*-
"""
Authors: Chris Falter, Johny Rufus John, and Xing Liu
Test the 15-tile puzzle solver code
"""
import unittest
from solver16 import findEmptySquare, isSolvable
import numpy as np

class TestSolver16(unittest.TestCase):
    
    def test_findEmptySquare_ReturnsLocationOfZeroValueElement(self):
        puzzle = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
        locationOfZero = findEmptySquare(puzzle)
        self.assertEquals(locationOfZero, (0,0))
        
    def test_isSolvable_WithUnsolvableState_ReturnsFalse(self):
        puzzle = np.array([[2,1,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
        self.assertFalse(isSolvable(puzzle))
        
    def test_isSolvable_WithSolvableState_ReturnsTrue(self):
        puzzle = np.array([[1,2,3,4],[7,5,6,12],[8,9,10,11],[13,14,15,0]])
        self.assertTrue(isSolvable(puzzle))

if __name__ == '__main__':
    unittest.main()

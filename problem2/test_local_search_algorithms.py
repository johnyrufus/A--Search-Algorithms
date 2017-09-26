#!/usr/bin/env python3
# test_local_search_algorithms.py : Test the local search algorithms
# Johny

import unittest
import sys
from assign import AssignmentSolver
from assign import AssignmentState
from assign import Group
from assign import User
from local_search_algorithms import LocalSearchAlgorithm
from local_search_algorithms import LocalSearchProblem
from local_search_algorithms import HillClimbing
from unittest import TestCase


class LocalSearchAlgorithmsTest(TestCase):

    def test_hill_climbing(self):
        inputs = AssignmentSolver.UserInputs('input.txt', 160, 31, 10, list(), [1])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = HillClimbing(problem)
        self.assertEqual(algorithm.search(), 1012)

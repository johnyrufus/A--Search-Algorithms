#!/usr/bin/env python3
# test_local_search_algorithms.py : Test the local search algorithms
# Johny

import unittest
import math
from assign import AssignmentSolver, AssignmentState, Group, User
from local_search_algorithms import LocalSearchAlgorithm, LocalSearchProblem, HillClimbing, \
    FirstChoiceHillClimbing, RandomRestartHillClimbing, HillClimbingWithSidewaysMove, HillClimbingWithRandomWalk, \
    SimulatedAnnealing
from unittest import TestCase


class LocalSearchAlgorithmsTest(TestCase):

    def test_hill_climbing1(self):
        inputs = AssignmentSolver.UserInputs('input.txt', 160, 31, 10, list(), [1])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = HillClimbing(problem)
        self.assertEqual(algorithm.search(), 1012)

    def test_hill_climbing2(self):
        min_res = math.inf
        for i in range(8):
            inputs = AssignmentSolver.UserInputs('input.txt', 160, 31, 10, list(), [3])
            problem = AssignmentSolver(inputs)
            problem.initialize()

            algorithm = HillClimbing(problem)
            res = algorithm.search()
            min_res = res if res < min_res else min_res
        self.assertEqual(min_res, 342)

    def test_first_choice_hill_climbing(self):
        min_res = math.inf
        for i in range(10):
            inputs = AssignmentSolver.UserInputs('input.txt', 160, 31, 10, list(), [3])
            problem = AssignmentSolver(inputs)
            problem.initialize()

            algorithm = FirstChoiceHillClimbing(problem)
            res = algorithm.search()
            min_res = res if res < min_res else min_res
            self.assertTrue(min_res < 500)

    def test_hill_climbing_with_sideways_moves(self):
        min_res = math.inf
        for i in range(8):
            inputs = AssignmentSolver.UserInputs('input.txt', 160, 31, 10, list(), [3])
            problem = AssignmentSolver(inputs)
            problem.initialize()

            algorithm = HillClimbingWithSidewaysMove(problem)
            res = algorithm.search()
            print(res)
            min_res = res if res < min_res else min_res
        self.assertEqual(min_res, 342)

    def test_hill_climbing_with_random_walk(self):
        min_res = math.inf
        for i in range(8):
            inputs = AssignmentSolver.UserInputs('input.txt', 160, 31, 10, list(), [3])
            problem = AssignmentSolver(inputs)
            problem.initialize()

            algorithm = HillClimbingWithRandomWalk(problem)
            res = algorithm.search()
            print(res)
            min_res = res if res < min_res else min_res
        self.assertEqual(min_res, 342)

    def test_random_restart_hill_climbing(self):
        inputs = AssignmentSolver.UserInputs('input.txt', 160, 31, 10, list(), [3])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = RandomRestartHillClimbing(problem, options={'nprocs': 8})
        res = algorithm.search()
        self.assertEqual(res, 342)

    def test_random_restart_hill_climbing_with_sideways_moves(self):
        inputs = AssignmentSolver.UserInputs('input.txt', 160, 31, 10, list(), [3])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = RandomRestartHillClimbing(problem, options={'nprocs': 8, 'sideways_moves': True})
        res = algorithm.search()
        self.assertEqual(res, 342)

    def test_random_restart_hill_climbing_with_random_walk(self):
        inputs = AssignmentSolver.UserInputs('input.txt', 160, 31, 10, list(), [3])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = RandomRestartHillClimbing(problem, options={'nprocs': 8, 'random_walk': True})
        res = algorithm.search()
        self.assertEqual(res, 342)

    def simulated_annealing_test_once(self):
        inputs = AssignmentSolver.UserInputs('input.txt', 160, 31, 10, list(), [3])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = SimulatedAnnealing(problem)
        res = algorithm.search()
        print(res)
        #self.assertEqual(res, 342)

    def test_simulated_annealing_repeated(self):
        for i in range(100):
            self.simulated_annealing_test_once()


if __name__ == '__main__':
    unittest.main()



#!/usr/bin/env python3
# test_local_search_algorithms.py : Test the local search algorithms
# Johny

import unittest
import math
from assign import AssignmentSolver, AssignmentState, Group, User, UserInputs
from local_search_algorithms import LocalSearchAlgorithm, LocalSearchProblem, HillClimbing, \
    FirstChoiceHillClimbing, RandomRestartHillClimbing, HillClimbingWithSidewaysMove, HillClimbingWithRandomWalk, \
    SimulatedAnnealing, RandomRestartHillClimbingHybrid
from unittest import TestCase

input_file = 'input_large_50.txt'
nprocs = 32

class LocalSearchAlgorithmsTest(TestCase):

    '''def test_hill_climbing1(self):
        inputs = UserInputs(input_file, 160, 31, 10, list(), [1])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = HillClimbing(problem)
        #self.assertEqual(algorithm.search().evaluate(), 1012)

    def test_hill_climbing2(self):
        min_res = math.inf
        print('hill_climbing ------ :')
        for i in range(10):
            inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
            problem = AssignmentSolver(inputs)
            problem.initialize()

            algorithm = HillClimbing(problem)
            res = algorithm.search().evaluate()
            min_res = res if res < min_res else min_res
            print(res)
        #self.assertEqual(min_res, 342)

    def test_first_choice_hill_climbing(self):
        min_res = math.inf
        print('first_choice_hill_climbing ------ :')
        for i in range(10):
            inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
            problem = AssignmentSolver(inputs)
            problem.initialize()

            algorithm = FirstChoiceHillClimbing(problem)
            res = algorithm.search().evaluate()
            min_res = res if res < min_res else min_res
            print(res)
            #self.assertTrue(min_res < 500)

    def test_hill_climbing_with_sideways_moves(self):
        min_res = math.inf
        print('test_hill_climbing_with_sideways_moves ------ :')
        for i in range(10):
            inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
            problem = AssignmentSolver(inputs)
            problem.initialize()

            algorithm = HillClimbingWithSidewaysMove(problem)
            res = algorithm.search().evaluate()
            print(res)
            min_res = res if res < min_res else min_res
        #self.assertEqual(min_res, 342)

    def test_hill_climbing_with_random_walk(self):
        min_res = math.inf
        print('test_hill_climbing_with_random_walk ------ :')
        for i in range(10):
            inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
            problem = AssignmentSolver(inputs)
            problem.initialize()

            algorithm = HillClimbingWithRandomWalk(problem)
            res = algorithm.search().evaluate()
            print(res)
            min_res = res if res < min_res else min_res
        #self.assertEqual(min_res, 342)'''

    def test_random_restart_hill_climbing(self):
        print('HC ------ :')
        inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = RandomRestartHillClimbing(problem, options={'nprocs': nprocs})
        res = algorithm.search().evaluate()
        print(res)
        #self.assertEqual(res, 342)

    def test_random_restart_hill_climbing_with_sideways_moves(self):
        print('Sideways ------ :')
        inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = RandomRestartHillClimbing(problem, options={'nprocs': nprocs, 'sideways_moves': True})
        res = algorithm.search().evaluate()
        print(res)
        #self.assertEqual(res, 342)

    def test_random_restart_hill_climbing_with_random_walk(self):
        print('Walk ------ :')
        inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = RandomRestartHillClimbing(problem, options={'nprocs': nprocs, 'random_walk': True})
        res = algorithm.search()
        print(res.evaluate())
        #self.assertEqual(res, 342)

    def test_random_restart_hill_climbing_hybrid(self):
        print('Hybrid ------ :')
        inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = RandomRestartHillClimbingHybrid(problem, options={'nprocs': nprocs})
        res = algorithm.search()
        print(res.evaluate())
        #self.assertEqual(res, 342)

    def simulated_annealing_test_once(self):
        inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
        problem = AssignmentSolver(inputs)
        problem.initialize()

        algorithm = SimulatedAnnealing(problem)
        res = algorithm.search().evaluate()
        return res
        #self.assertEqual(res, 342)

    def test_simulated_annealing_repeated(self):
        print('sim ann ------ :')
        res = min(self.simulated_annealing_test_once() for x in range(32))
        print(res)
        # self.assertEqual(res, 342)

if __name__ == '__main__':
    unittest.main()



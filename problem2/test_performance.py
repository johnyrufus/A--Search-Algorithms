#!/usr/bin/env python3
# test_performance.py : Test the local search algorithms performance
# Johny

import unittest
import math
import time
from assign import AssignmentSolver, AssignmentState, Group, User, UserInputs
from local_search_algorithms import LocalSearchAlgorithm, LocalSearchProblem, HillClimbing, \
    FirstChoiceHillClimbing, RandomRestartHillClimbing, HillClimbingWithSidewaysMove, HillClimbingWithRandomWalk, \
    SimulatedAnnealing, RandomRestartHillClimbingHybrid
from unittest import TestCase

input_file = 'input_large_10.txt'
nprocs = 32




def test_random_restart_hill_climbing_with_sideways_moves():
    inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
    problem = AssignmentSolver(inputs)
    problem.initialize()

    algorithm = RandomRestartHillClimbing(problem, options={'nprocs': nprocs, 'sideways_moves': True})
    res = algorithm.search().evaluate()
    return res

def test_random_restart_hill_climbing_with_random_walk():
    inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
    problem = AssignmentSolver(inputs)
    problem.initialize()

    algorithm = RandomRestartHillClimbing(problem, options={'nprocs': nprocs, 'random_walk': True})
    res = algorithm.search().evaluate()
    return res

def test_random_restart_hill_climbing_hybrid():
    inputs = UserInputs(input_file, 160, 31, 10, list(), [3])
    problem = AssignmentSolver(inputs)
    problem.initialize()

    algorithm = RandomRestartHillClimbingHybrid(problem, options={'nprocs': nprocs})
    res = algorithm.search().evaluate()
    return res



if __name__ == '__main__':

    counts = {'sideways':0, 'walk':0, 'hybrid':0}
    stime = [0] * 20
    wtime = [0] * 20
    htime = [0] * 20

    for i in range(20):

        start = time.clock()
        s = test_random_restart_hill_climbing_with_sideways_moves()
        stime[i] += time.clock() - start

        start = time.clock()
        w = test_random_restart_hill_climbing_with_random_walk()
        wtime[i] += time.clock() - start

        start = time.clock()
        h = test_random_restart_hill_climbing_hybrid()
        htime[i] += time.clock() - start

        if s <= w and s <= h:
            counts['sideways'] += 1
        if w <= s and w <= h:
            counts['walk'] += 1
        if h <= s and h <= w:
            counts['hybrid'] += 1

    print(counts)
    print('Time taken - sideways - {}, walk - {}, hybrid - {}'.format(sum(stime)/20.0, sum(wtime)/20.0, sum(htime)/20.0))
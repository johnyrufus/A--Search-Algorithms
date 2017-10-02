#!/usr/bin/env python3
# local_search_algorithms.py : Implement the local search algorithms
# Johny

import abc
from multiprocessing import Queue, Process, Pool

import random
import math
import sys
import copy


# Base class for all search algorithms.
class LocalSearchAlgorithm:
    def __init__(self, problem, options=None):
        self.problem = problem
        self.options = options if options else {}

    def search(self):
        pass


# Base class for search problem.
class LocalSearchProblem:
    def __init__(self, state=None):
        self.state = state

    @abc.abstractmethod
    def next_neighbor(self):
        return

    @abc.abstractmethod
    def next_neighbor_for_user(self, user_index):
        return

    @abc.abstractmethod
    def initialize(self):
        return


# Hill climbing algorithm
class HillClimbing(LocalSearchAlgorithm):

    def search(self):
        next_state = self.problem.state
        while next_state:
            self.problem.state = next_state
            neighbor_min_state = self.problem.state
            next_state = None
            neighbor = self.problem.state.next_neighbor()
            while neighbor:
                if neighbor.evaluate() < neighbor_min_state.evaluate():
                    neighbor_min_state = neighbor
                neighbor = self.problem.state.next_neighbor()
            if neighbor_min_state is not self.problem.state:
                next_state = neighbor_min_state
        return self.problem.state


# Hill climbing algorithm with sideways moves permitted.
class HillClimbingWithSidewaysMove(LocalSearchAlgorithm):

    def search(self):
        max_sideways_moves = self.options.get('sideways_moves', 100)
        sideways_moves = 0
        next_state = self.problem.state
        while True:
            self.problem.state = next_state
            neighbor_min_state = self.problem.state
            neighbor = self.problem.state.next_neighbor()
            while neighbor:
                if neighbor.evaluate() <= neighbor_min_state.evaluate():
                    neighbor_min_state = neighbor
                neighbor = self.problem.state.next_neighbor()
            if neighbor_min_state is self.problem.state:
                break
            if neighbor_min_state.evaluate() == self.problem.state.evaluate():
                if sideways_moves == max_sideways_moves:
                    break
                else:
                    sideways_moves += 1
            else:
                sideways_moves = 0
            next_state = neighbor_min_state
        return self.problem.state


# First choice Hill climbing algorithm
class FirstChoiceHillClimbing(LocalSearchAlgorithm):

    def search(self):
        next_state = self.problem.state
        while next_state:
            self.problem.state = next_state
            neighbor_min_state = self.problem.state
            next_state = None
            neighbor = self.problem.state.next_neighbor()
            while neighbor:
                if neighbor.evaluate() < neighbor_min_state.evaluate():
                    neighbor_min_state = neighbor
                    break
                neighbor = self.problem.state.next_neighbor()
            if neighbor_min_state is not self.problem.state:
                next_state = neighbor_min_state
        return self.problem.state


# Hill climbing algorithm with random walks permitted.
class HillClimbingWithRandomWalk(LocalSearchAlgorithm):

    def search(self):
        probability = self.options.get('probability', 0.80)
        next_state = self.problem.state
        while next_state:
            self.problem.state = next_state
            neighbor_min_state = self.problem.state
            next_state = None
            neighbor = self.problem.state.next_neighbor()
            if random.random() > probability:
                next_state = neighbor
                continue
            while neighbor:
                if neighbor.evaluate() < neighbor_min_state.evaluate():
                    neighbor_min_state = neighbor
                neighbor = self.problem.state.next_neighbor()
            if neighbor_min_state is not self.problem.state:
                next_state = neighbor_min_state
        return self.problem.state


# Parallel Random restart hill climbing algorithm, with options for sideways moves or random walk
class RandomRestartHillClimbing(LocalSearchAlgorithm):

    def worker(self, q):
        self.problem.initialize()
        if self.options.get('sideways_moves', False):
            algorithm = HillClimbingWithSidewaysMove
        elif self.options.get('random_walk', False):
            algorithm = HillClimbingWithRandomWalk
        else:
            algorithm = HillClimbing
        res = algorithm(self.problem).search()
        q.put(res)

    def search(self):
        q = Queue()
        nprocs = self.options['nprocs'] if 'nprocs' in self.options else 32
        procs = list()
        for i in range(nprocs):
            p = Process(target=self.worker, args=(q,))
            procs.append(p)
            p.start()

        res = [q.get() for _ in range(nprocs)]
        #print(res)
        for p in procs:
            p.join()
        return min(res, key=lambda x: x.evaluate())


# Parallel Random restart hill climbing algorithm, with both sideways moves and random walk hybrid
class RandomRestartHillClimbingHybrid(LocalSearchAlgorithm):

    def worker(self, q, i):
        algorithms = {0: HillClimbingWithRandomWalk, 1: HillClimbingWithSidewaysMove, 2: HillClimbingWithSidewaysMove, 3: HillClimbingWithSidewaysMove}
        self.problem.initialize()
        algorithm = algorithms[i%4]
        res = algorithm(self.problem).search()
        q.put(res)

    def search(self):
        q = Queue()
        nprocs = self.options['nprocs'] if 'nprocs' in self.options else 32
        procs = list()
        for i in range(nprocs):
            p = Process(target=self.worker, args=(q, i))
            procs.append(p)
            p.start()

        res = [q.get() for _ in range(nprocs)]
        #print(res)
        for p in procs:
            p.join()
        return min(res, key=lambda x: x.evaluate())


# Simulated Annealing
class SimulatedAnnealing(LocalSearchAlgorithm):

    def search(self):
        next_state = self.problem.state
        for t in range(1, sys.maxsize):
            T = self.exp_schedule(t)
            if T > 0 and next_state:
                #print(T)
                self.problem.state = next_state
                next_state = None
                neighbor = self.problem.state.next_neighbor()
                while neighbor:
                    delta_e = self.problem.state.evaluate() - neighbor.evaluate()
                    if delta_e > 0 or math.exp(delta_e / T) > random.uniform(0.0, 1.0):
                        next_state = neighbor
                        break
                    neighbor = self.problem.state.next_neighbor()
            else:
                break
        return self.problem.state

    # Simulate Annealing schedule function referred from textbook code - https://github.com/aimacode/
    def exp_schedule(self, t, k=20, lam=0.005, limit=100):
        #print(t)
        return k * math.exp(-lam * t) if t < limit else 0







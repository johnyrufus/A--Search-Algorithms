#!/usr/bin/env python3
# local_search_algorithms.py : Implement the local search algorithms
# Johny

import abc
from multiprocessing import Queue, Process, Pool


class LocalSearchAlgorithm:
    def __init__(self, problem, options=None):
        self.problem = problem
        self.options = options

    def search(self):
        pass


class LocalSearchProblem:
    def __init__(self, state=None):
        self.state = state

    @abc.abstractmethod
    def next_neighbor(self):
        return

    @abc.abstractmethod
    def initialize(self):
        return


class HillClimbing(LocalSearchAlgorithm):

    def search(self):
        next_state = self.problem.state
        while next_state is not None:
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
        return self.problem.state.evaluate()


class HillClimbingWithSidewaysMove(LocalSearchAlgorithm):

    def search(self):
        max_sideways_moves = self.options['sideways_moves'] if self.options is not None else 100
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
        return self.problem.state.evaluate()


class FirstChoiceHillClimbing(LocalSearchAlgorithm):

    def search(self):
        next_state = self.problem.state
        while next_state is not None:
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
        return self.problem.state.evaluate()


class RandomRestartHillClimbing(LocalSearchAlgorithm):

    def worker(self, q):
        self.problem.initialize()
        algorithm = None
        if self.options is not None and 'sideways_moves' in self.options and self.options['sideways_moves'] == True:
            algorithm = HillClimbingWithSidewaysMove
        else:
            algorithm = HillClimbing
        res = algorithm(self.problem).search()
        q.put(res)

    def search(self):
        q = Queue()
        nprocs = self.options['nprocs'] if 'nprocs' in self.options else 16
        procs = list()
        for i in range(nprocs):
            p = Process(target=self.worker, args=(q,))
            procs.append(p)
            p.start()

        res = [q.get() for _ in range(nprocs)]
        print(res)
        for p in procs:
            p.join()
        return min(res)





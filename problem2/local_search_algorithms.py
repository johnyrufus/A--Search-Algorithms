#!/usr/bin/env python3
# local_search_algorithms.py : Implement the local search algorithms
# Johny

import abc

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

class HillClimbing(LocalSearchAlgorithm):

    def search(self):
        next_state = self.problem.state
        while next_state is not None:
            self.problem.state = next_state
            next_state = None
            neighbor = self.problem.state.next_neighbor()
            while neighbor:
                if next_state is not None and neighbor.evaluate() > next_state.evaluate():
                    next_state = neighbor
                neighbor = self.problem.state.next_neighbor()
        return self.problem.state.evaluate()




#!/usr/bin/env python3
# assign.py : Solve the assignment problem
# Johny

import sys
import random
from datetime import datetime
from collections import namedtuple
from functools import reduce
from itertools import product
from local_search_algorithms import LocalSearchProblem


class User:
    def __init__(self, user_id, group_size=0, favorites=set(), oops=set()):
        self.user_id = user_id
        self.favorites = favorites
        self.group_size = group_size
        self.oops = oops

    def __repr__(self):
        return "{} - {} - {} - {}".format(self.user_id, self.group_size, self.favorites, self.oops)


class Group:
    def __init__(self, members):
        self.members = members

    def __repr__(self):
        return "Members - {}, Score - {} \n".format([m.user_id for m in self.members], self.evaluate())

    def evaluate(self, inputs):
        fav_count = 0
        oops_count = 0
        for user1, user2 in product(self.members, self.members):
            if user1 != user2:
                fav_count += 1 if user2.user_id in user1.favorites else 0
                oops_count += 1 if user2.user_id in user1.oops else 0
        group_fav_count = reduce(lambda acc, m: acc + len(m.favorites), self.members, 0)
        return (group_fav_count - fav_count) * inputs.n + oops_count * inputs.m + reduce(
            lambda acc, m: acc + (0 if m.group_size == 0 or m.group_size == len(self.members) else 1), self.members, 0)


class AssignmentState:
    def __init__(self, inputs, groups=None):
        if groups is None:
            self.groups = [Group(list())]
        else:
            self.groups = groups
        self.solution = None
        self.inputs = inputs
        self.explored_neighbors = set()

    def __repr__(self):
        return "Groups - {}, Explored Neighbors - {} \n".format(self.groups, self.explored_neighbors)

    def assign_user_to_group(self, user, group):
        if len(group.members) == self.inputs.max_members_in_group[0] or user in group.members:
            return None
        return self.create_new_state(user, group)

    def create_new_state(self, remove_user, move_to_group):
        new_groups = list()
        for group in self.groups:
            if remove_user in group.members:
                if len(group.members) > 1:
                    index = group.members.index(remove_user)
                    new_members = group.members[:index] + group.members[index+1:]
                    new_groups.append(Group(new_members))
                elif len(group.members) == 1 and len(move_to_group.members) == 0:
                    return None
            elif group == move_to_group:
                if len(move_to_group.members) == 0:
                    new_groups.append(group)
                new_groups.append(Group(group.members[:] + [remove_user]))
            else:
                new_groups.append(group)
        return AssignmentState(self.inputs, new_groups)

    def get_next_random_state(self):
        while not self.is_fully_explored():
            m = random.randint(0, len(self.inputs.users)-1)
            n = random.randint(0, len(self.groups)-1)
            s = '{}-{}'.format(m, n)
            if not s in self.explored_neighbors:
                self.explored_neighbors.add(s)
                next_state = self.assign_user_to_group(self.inputs.users[m], self.groups[n])
                if next_state:
                    return next_state

    def is_fully_explored(self):
        return len(self.inputs.users) * len(self.groups) == len(self.explored_neighbors)

    def evaluate(self):
        if not self.solution:
            solution = (len(self.groups) - 1) * self.inputs.k + reduce(lambda acc, g: acc + g.evaluate(self.inputs), self.groups, 0)
        return solution

    def next_neighbor(self):
        return self.get_next_random_state()


class AssignmentSolver(LocalSearchProblem):
    UserInputs = namedtuple('UserInputs', 'input_file k m n users max_members_in_group')

    def __init__(self, user_inputs = None):
        self.user_inputs = user_inputs if user_inputs else self.get_inputs_from_user()
        super().__init__(AssignmentState(self.user_inputs))

    def get_inputs_from_user(self):
        return AssignmentSolver.UserInputs(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], list(), list())

    def initialize(self):
        random.seed(datetime.now())
        del self.user_inputs.users[:]
        self.state = AssignmentState(self.user_inputs)

        with open(self.user_inputs.input_file, 'r') as f:
            for line in f:
                tokens = line.split()
                favorites = set(tokens[2].split(',')) if tokens[2] != '_' else set()
                oops = set(tokens[3].split(',')) if tokens[3] != '_' else set()
                user = User(tokens[0], int(tokens[1]), favorites, oops)
                self.user_inputs.users.append(user)
                while True:
                    group = self.state.groups[random.randint(0, len(self.state.groups) - 1)]
                    new_state = self.state.assign_user_to_group(user, group)
                    if new_state:
                        self.state = new_state
                        break


def main():
    solver = AssignmentSolver()


if __name__ == '__main__':
    main()



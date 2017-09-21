#!/usr/bin/env python3
# assign.py : Solve the assignment problem
# Johny

import sys
import random
from collections import defaultdict as hashmap
from functools import reduce
from itertools import product
import unittest


class User:
    def __init__(self, _user_id, _group_size=0, _favorites=set(), _oops=set()):
        self.user_id = _user_id
        self.favorites = _favorites
        self.group_size = _group_size
        self.oops = _oops
        self.group = -1

    def __repr__(self):
        return "{} - {} - {} - {}".format(self.user_id, self.group_size, self.favorites, self.oops)

    def assign_user_to_group(self, _group):
        self.group = _group


class Group:
    def __init__(self, _members):
        self.members = _members
        self.score = 0

    def __repr__(self):
        return "Members - {}, Score - {} \n".format([m.user_id for m in self.members], self.score)

    def evaluate(self):
        solver = AssignmentSolver
        self.score = 0
        fav_count = 0
        oops_count = 0
        for user1, user2 in product(self.members, self.members):
            if user1 != user2:
                fav_count += 1 if user2.user_id in user1.favorites else 0
                oops_count += 1 if user2.user_id in user1.oops else 0
        group_fav_count = reduce(lambda acc, m: acc + len(m.favorites), self.members, 0)
        print(group_fav_count)
        self.score = (group_fav_count - fav_count) * solver.n + oops_count * solver.m + reduce(
            lambda acc, m: acc + (0 if m.group_size == 0 or m.group_size == len(self.members) else 1), self.members, 0)

    def assign_user_to_group(self, user):
        solver = AssignmentSolver
        if len(self.members) == solver.max_members_in_group:
            return False
        if self == solver.empty_group:
            return solver.create_group().assign_user_to_group(user)
        self.members.append(user)
        user.assign_user_to_group(self)
        self.evaluate()
        return True


class AssignmentSolver:
    users = list()
    empty_group = Group(list())
    groups = [empty_group]
    max_members_in_group = 3 # change this to 3 in the end
    input_file = 'input.txt'
    k = 0
    m = 0
    n = 0

    @classmethod
    def get_inputs_from_user(cls):
        cls.input_file = sys.argv[1]
        cls.k = int(sys.argv[2])
        cls.m = int(sys.argv[3])
        cls.n = int(sys.argv[4])

    @classmethod
    def initialize(cls):

        with open(cls.input_file, 'r') as f:
            for line in f:
                tokens = line.split()
                favorites = set(tokens[2].split(',')) if tokens[2] != '_' else set()
                oops = set(tokens[3].split(',')) if tokens[3] != '_' else set()
                user = User(tokens[0], int(tokens[1]), favorites, oops)
                cls.users.append(user)
                while True:
                    group = cls.groups[random.randint(0, len(cls.groups) - 1)]
                    if group.assign_user_to_group(user):
                        break

        # for evaluate_cost(): group in groups, group.evaluate() and calc formula
        print(cls.groups)
        print(cls.users)

    @classmethod
    def create_group(cls):
        group = Group(list())
        cls.groups.append(group)
        return group

    @classmethod
    def calculate_time(cls):
        return (len(cls.groups) - 1) * cls.k + reduce(lambda acc, g: acc + g.score, cls.groups, 0)


def main():
    AssignmentSolver.get_inputs_from_user()
    AssignmentSolver.max_members_in_group = 1
    AssignmentSolver.initialize()


if __name__ == '__main__':
    main()



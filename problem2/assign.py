#!/usr/bin/env python3
# assign.py : Solve the assignment problem
# Johny

import sys
import random
from functools import reduce
from itertools import product


class User:
    def __init__(self, _user_id, _group_size=0, _favorites=set(), _oops=set()):
        self.user_id = _user_id
        self.favorites = _favorites
        self.group_size = _group_size
        self.oops = _oops

    def __repr__(self):
        return "{} - {} - {} - {}".format(self.user_id, self.group_size, self.favorites, self.oops)


class Group:
    def __init__(self, _members):
        self.members = _members

    def __repr__(self):
        return "Members - {}, Score - {} \n".format([m.user_id for m in self.members], self.evaluate())

    def evaluate(self):
        solver = AssignmentSolver
        fav_count = 0
        oops_count = 0
        for user1, user2 in product(self.members, self.members):
            if user1 != user2:
                fav_count += 1 if user2.user_id in user1.favorites else 0
                oops_count += 1 if user2.user_id in user1.oops else 0
        group_fav_count = reduce(lambda acc, m: acc + len(m.favorites), self.members, 0)
        print(group_fav_count)
        return (group_fav_count - fav_count) * solver.n + oops_count * solver.m + reduce(
            lambda acc, m: acc + (0 if m.group_size == 0 or m.group_size == len(self.members) else 1), self.members, 0)


class AssignmentState:
    def __init__(self, _groups=None):
        if _groups is None:
            self.groups = [Group(list())]
        else:
            self.groups = _groups
        self.explored_neighbors = set()

    def __repr__(self):
        return "Groups - {}, Explored Neighbors - {} \n".format(self.groups, self.explored_neighbors)

    def assign_user_to_group(self, user, group):
        solver = AssignmentSolver
        if len(group.members) == solver.max_members_in_group or user in group.members:
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
        return AssignmentState(new_groups)

    def get_next_random_state(self):
        solver = AssignmentSolver
        while not self.is_fully_explored():
            print('users -- randome before')
            m = random.randint(0, len(solver.users)-1)
            print('groups -- randome before' + str(len(self.groups)))
            n = random.randint(0, len(self.groups)-1)
            print('groups -- randome after' + str(len(self.groups)))
            s = '{}-{}'.format(m, n)
            print(self.explored_neighbors)
            if not s in self.explored_neighbors:
                self.explored_neighbors.add(s)
                next_state = self.assign_user_to_group(solver.users[m], self.groups[n])
                if next_state:
                    return next_state

    def is_fully_explored(self):
        print(len(self.explored_neighbors))
        return len(AssignmentSolver.users) * len(self.groups) == len(self.explored_neighbors)

    def evaluate(self):
        return (len(self.groups) - 1) * AssignmentSolver.k + reduce(lambda acc, g: acc + g.evaluate(), self.groups, 0)


class AssignmentSolver:
    users, state = list(), AssignmentState()
    input_file, max_members_in_group = 'input.txt', 3 # change this to 3 in the end
    k, m, n = 0, 0, 0

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
                    group = cls.state.groups[random.randint(0, len(cls.state.groups) - 1)]
                    new_state = cls.state.assign_user_to_group(user, group)
                    if new_state:
                        cls.state = new_state
                        break
        print(cls.state)
        print(cls.users)


# TODO:
class RandomNeighborGenerator:
    def __init__(self, _users, _groups):
        self.users = _users
        self.groups = _groups
        self.visited = {}


def main():
    AssignmentSolver.get_inputs_from_user()
    AssignmentSolver.max_members_in_group = 1
    AssignmentSolver.initialize()


if __name__ == '__main__':
    main()



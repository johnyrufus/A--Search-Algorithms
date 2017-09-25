#!/usr/bin/env python3

import unittest
import sys
from assign import AssignmentSolver
from assign import AssignmentState
from assign import Group
from assign import User
from unittest import TestCase


class AssignmentSolverTest(TestCase):

    def test_basic_groups1(self):
        solver = AssignmentSolver
        solver.max_members_in_group = 1
        solver.k, solver.m, solver.n = 160, 31, 10
        solver.users = []
        solver.state = AssignmentState()
        solver.initialize()

        self.assertEqual(len(solver.state.groups), len(solver.users) + 1)
        self.assertEqual(len(solver.users), 6)
        self.assertEqual(sorted([g.evaluate() for g in solver.state.groups]), [0,0,0,0,10,21,21])
        self.assertEqual(solver.state.evaluate(), 1012)

    def test_basic_groups2(self):
        solver = AssignmentSolver
        solver.max_members_in_group = 3
        solver.k, solver.m, solver.n = 160, 31, 10
        solver.users = []
        solver.state = AssignmentState()
        solver.initialize()

        list1, list2, list3 = list(), list(), list()

        for user in solver.users:
            if user.user_id == 'djcran' or user.user_id == 'chen464':
                list1.append(user)
            elif user.user_id == 'kapadia' or user.user_id == 'zehzhang' or user.user_id == 'fan6':
                list2.append(user)
            elif user.user_id == 'steflee':
                list3.append(user)

        solver.state = AssignmentState([Group(list()), Group(list1), Group(list2), Group(list3)])

        self.assertEqual(len(solver.state.groups), 4)
        self.assertEqual(len(solver.users), 6)
        self.assertEqual(sorted([g.evaluate() for g in solver.state.groups]), [0,0,12,42])
        self.assertEqual(solver.state.evaluate(), 534)

    def test_assign_user_to_group(self):
        solver = AssignmentSolver
        solver.max_members_in_group = 3
        solver.k, solver.m, solver.n = 160, 31, 10
        solver.users = []
        solver.state = AssignmentState()
        solver.initialize()

        solver.state = AssignmentState()

        solver.state = solver.state.assign_user_to_group(self.get_user('djcran', solver.users), solver.state.groups[0])
        self.assertEqual(solver.state.groups[1].evaluate(), 21)
        self.assertEqual(solver.state.evaluate(), 181)

        solver.state = solver.state.assign_user_to_group(self.get_user('chen464', solver.users), solver.state.groups[1])
        self.assertEqual(solver.state.evaluate(), 172)

        solver.state = solver.state.assign_user_to_group(self.get_user('kapadia', solver.users), solver.state.groups[0])
        self.assertEqual(solver.state.evaluate(), 353)

        solver.state = solver.state.assign_user_to_group(self.get_user('zehzhang', solver.users), solver.state.groups[1])
        self.assertEqual(solver.state.evaluate(), 375)

    def test_state_generation1(self):
        solver = AssignmentSolver
        solver.input_file = 'input.txt'
        solver.max_members_in_group = 1
        solver.k, solver.m, solver.n = 160, 31, 10
        solver.users = []
        solver.state = AssignmentState()
        solver.initialize()
        solver.max_members_in_group = 3

        next_state = solver.state.get_next_random_state()
        count = 0
        while next_state:
            count += 1
            print('count is - ' + str(count))
            next_state = solver.state.get_next_random_state()
        self.assertEqual(count, 30)

    def test_state_generation2(self):
        solver = AssignmentSolver
        solver.input_file = 'input_small.txt'
        solver.max_members_in_group = 1
        solver.k, solver.m, solver.n = 160, 31, 10
        solver.users = []
        solver.state = AssignmentState()
        solver.initialize()
        solver.max_members_in_group = 3

        next_state = solver.state.get_next_random_state()
        count = 0
        while next_state:
            count += 1
            print('count is - ' + str(count))
            next_state = solver.state.get_next_random_state()
        self.assertEqual(count, 2)

    def get_user(self, user_id, users):
        return [user for user in users if user.user_id == user_id][0]

if __name__ == '__main__':
    unittest.main()

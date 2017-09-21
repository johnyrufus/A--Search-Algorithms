#!/usr/bin/env python3

import unittest
import sys
from assign import AssignmentSolver
from assign import Group
from assign import User
from unittest import TestCase
if __name__ == '__main__':
    unittest.main()


class AssignmentSolverTest(TestCase):

    def test_basic_groups1(self):
        print(sys.path)
        solver = AssignmentSolver
        solver.max_members_in_group = 1
        solver.k = 160
        solver.m = 31
        solver.n = 10
        solver.initialize()

        self.assertEqual(len(solver.groups), len(solver.users) + 1)
        self.assertEqual(len(solver.users), 6)
        self.assertEqual(sorted([g.score for g in solver.groups]), [0,0,0,0,10,21,21])
        self.assertEqual(solver.calculate_time(), 1012)

    def test_basic_groups2(self):
        print(sys.path)
        solver = AssignmentSolver
        solver.max_members_in_group = 3
        solver.k = 160
        solver.m = 31
        solver.n = 10
        solver.users = []
        solver.initialize()

        solver.groups = [solver.create_group()]
        group1 = solver.create_group()
        group2 = solver.create_group()
        group3 = solver.create_group()

        for user in solver.users:
            if user.user_id == 'djcran' or user.user_id == 'chen464':
                group1.assign_user_to_group(user)
            elif user.user_id == 'kapadia' or user.user_id == 'zehzhang' or user.user_id == 'fan6':
                group2.assign_user_to_group(user)
            elif user.user_id == 'steflee':
                group3.assign_user_to_group(user)

        self.assertEqual(len(solver.groups), 4)
        self.assertEqual(len(solver.users), 6)
        self.assertEqual(sorted([g.score for g in solver.groups]), [0,0,12,42])
        self.assertEqual(solver.calculate_time(), 534)

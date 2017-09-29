#!/usr/bin/env python3
# test_assign.py : Test the assignment problem
# Johny

import unittest
from assign import AssignmentSolver, AssignmentState, Group, User, UserInputs
from unittest import TestCase


class AssignmentSolverTest(TestCase):

    def test_basic_groups1(self):
        inputs = UserInputs('input.txt', 160, 31, 10, list(), [1])
        solver = AssignmentSolver(inputs)
        solver.initialize()

        self.assertEqual(len(solver.state.groups), len(inputs.users) + 1)
        self.assertEqual(len(inputs.users), 6)
        self.assertEqual(sorted([g.evaluate(inputs) for g in solver.state.groups]), [0,0,0,0,10,21,21])
        self.assertEqual(solver.state.evaluate(), 1012)

    def test_basic_groups2(self):
        inputs = UserInputs('input.txt', 160, 31, 10, list(), [3])
        solver = AssignmentSolver(inputs)
        solver.initialize()

        list1, list2, list3 = list(), list(), list()

        for user in inputs.users:
            if user.user_id == 'djcran' or user.user_id == 'chen464':
                list1.append(user)
            elif user.user_id == 'kapadia' or user.user_id == 'zehzhang' or user.user_id == 'fan6':
                list2.append(user)
            elif user.user_id == 'steflee':
                list3.append(user)

        solver.state = AssignmentState(inputs, [Group(list()), Group(list1), Group(list2), Group(list3)])

        self.assertEqual(len(solver.state.groups), 4)
        self.assertEqual(len(inputs.users), 6)
        self.assertEqual(sorted([g.evaluate(inputs) for g in solver.state.groups]), [0,0,12,42])
        self.assertEqual(solver.state.evaluate(), 534)

    def test_assign_user_to_group(self):
        inputs = UserInputs('input.txt', 160, 31, 10, list(), [3])
        solver = AssignmentSolver(inputs)
        solver.initialize()

        solver.state = AssignmentState(inputs)

        solver.state = solver.state.assign_user_to_group(self.get_user('djcran', inputs.users), solver.state.groups[0])
        self.assertEqual(solver.state.groups[1].evaluate(inputs), 21)
        self.assertEqual(solver.state.evaluate(), 181)

        solver.state = solver.state.assign_user_to_group(self.get_user('chen464', inputs.users), solver.state.groups[1])
        self.assertEqual(solver.state.evaluate(), 172)

        solver.state = solver.state.assign_user_to_group(self.get_user('kapadia', inputs.users), solver.state.groups[0])
        self.assertEqual(solver.state.evaluate(), 353)

        solver.state = solver.state.assign_user_to_group(self.get_user('zehzhang', inputs.users), solver.state.groups[1])
        self.assertEqual(solver.state.evaluate(), 375)

    def test_state_generation1(self):
        inputs = UserInputs('input.txt', 160, 31, 10, list(), [1])
        solver = AssignmentSolver(inputs)
        solver.initialize()

        inputs = UserInputs('input.txt', 160, 31, 10, inputs.users, [3])
        solver.inputs = inputs
        solver.state.inputs = inputs

        next_state = solver.state.get_next_random_state()
        count = 0
        while next_state:
            count += 1
            next_state = solver.state.get_next_random_state()
        self.assertEqual(count, 30)

    def test_state_generation2(self):
        inputs = UserInputs('input_small.txt', 160, 31, 10, list(), [1])
        solver = AssignmentSolver(inputs)
        solver.initialize()

        inputs = UserInputs('input_small.txt', 160, 31, 10, inputs.users, [3])
        solver.inputs = inputs
        solver.state.inputs = inputs

        next_state = solver.state.get_next_random_state()
        count = 0
        while next_state:
            count += 1
            next_state = solver.state.get_next_random_state()
        self.assertEqual(count, 2)

    def get_user(self, user_id, users):
        return [user for user in users if user.user_id == user_id][0]

if __name__ == '__main__':
    unittest.main()

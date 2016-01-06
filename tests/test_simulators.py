from __future__ import absolute_import

import unittest

import pyrtl
from johnlib import simulators


class TestCheckEquivalence(unittest.TestCase):

    def setUp(self):
        pyrtl.reset_working_block()

    def test_equivalence_pass(self):
        a, b = pyrtl.Input(1, 'a'), pyrtl.Input(1, 'b')
        out = pyrtl.Output(1, 'out')
        out <<= a & b
        self.assertTrue(simulators.circuit_equivalence(lambda i, j: i & j))

    def test_equivalence_fail(self):
        a, b = pyrtl.Input(1, 'a'), pyrtl.Input(1, 'b')
        out = pyrtl.Output(1, 'out')
        out <<= a & b

        def soft_or(a, b):
            return a | b

        self.assertFalse(simulators.circuit_equivalence(soft_or))

    def test_equivalence_asymetrical(self):
        a, b = pyrtl.Input(1, 'a'), pyrtl.Input(1, 'b')
        out = pyrtl.Output(1, 'out')
        out <<= a & ~b
        self.assertFalse(simulators.circuit_equivalence(lambda i, j: i ^ ~j))

    def test_longer_wires(self):
        a = pyrtl.Input(3, 'a')
        b = pyrtl.Input(2, 'b')
        out = pyrtl.Output(name='out')
        out <<= a + b
        pyrtl.synthesize()
        self.assertTrue(simulators.circuit_equivalence(lambda i, j: i + j, in_wires=(a, b)))


class TestGetInputs(unittest.TestCase):
    def setUp(self):
        pyrtl.reset_working_block()
        self.block = pyrtl.working_block()

    def test_autogen(self):
        a = pyrtl.Input()
        self.assertEquals(simulators._get_inputs(None, self.block), [a])

    def test_specified(self):
        a = pyrtl.Input()
        b = pyrtl.Input()
        self.assertEquals(simulators._get_inputs([a], self.block), [a])

    def test_sorted(self):
        a = pyrtl.Input(name='a')
        b = pyrtl.Input(name='b')
        self.assertEquals(simulators._get_inputs(None, self.block), [a, b])


class TestGetOutputs(unittest.TestCase):
    def setUp(self):
        pyrtl.reset_working_block()
        self.block = pyrtl.working_block()

    def test_no_outputs(self):
        with self.assertRaises(pyrtl.PyrtlError):
            simulators._get_output(None, self.block)

    def test_too_many_outputs(self):
        a = pyrtl.Output()
        b = pyrtl.Output()
        with self.assertRaises(pyrtl.PyrtlError):
            simulators._get_output(None, self.block)

    def test_autogen(self):
        a = pyrtl.Output()
        self.assertIs(simulators._get_output(None, self.block), a)

    def test_invalid_specification(self):
        with self.assertRaises(pyrtl.PyrtlError):
            simulators._get_output(1, self.block)

    def test_specified(self):
        a = pyrtl.Output()
        b = pyrtl.Output()
        self.assertIs(simulators._get_output(b, self.block), b)

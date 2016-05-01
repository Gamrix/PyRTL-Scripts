import unittest
from JohnLib.graphs import graphBase


class TestAttrs(unittest.TestCase):

    def test_add_empty_attr(self):
        expected = {'a': {'b': 'c'}}
        actual = graphBase.add_attr({}, 'b', 'c', 'a')
        self.assertEqual(actual, expected)

    def test_add_existing_attr(self):
        original = {'a': {'b': 'c'}}
        expected = {'a': {'b': 'c', 'c': 'd'}}
        actual = graphBase.add_attr(original, 'c', 'd', 'a')
        self.assertEqual(actual, expected)

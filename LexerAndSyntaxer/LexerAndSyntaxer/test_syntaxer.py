import unittest
from Syntaxer.SyntaxAnalyzer import *

class Test_UniformRules(unittest.TestCase):

    def test_rules_sorted(self):
        testing = [
            ["A", ["b A"]],
            ["A", ["b B"]],
            ["B", ["b A"]],
            ["B", ["b B"]],
            ["C", ["b A"]],
            ["C", ["b B"]]
        ]

        expected = [
            ["A", ["b A", "b B"]],
            ["B", ["b A", "b B"]],
            ["C", ["b A", "b B"]]
        ]

        actual = UniformRules(testing)
        self.assertEqual(expected, actual, "UniformRules can't do simplest task")

    def test_rules_not_sorted(self):
        testing = [
            ["A", ["b A"]],
            ["B", ["b A"]],
            ["A", ["b B"]],
            ["B", ["b B"]],
            ["C", ["b A"]],
            ["C", ["b B"]]
        ]

        expected = [
            ["A", ["b A", "b B"]],
            ["B", ["b A", "b B"]],
            ["C", ["b A", "b B"]]
        ]

        actual = UniformRules(testing)
        self.assertEqual(expected, actual, "UniformRules can't do unsorted rules")

    def test_rules_partially_uniformed(self):
        testing = [
            ["A", ["b A", "b B"]],
            ["B", ["b B"]],
            ["B", ["b A"]],
            ["C", ["b A"]],
            ["C", ["b B"]]
        ]

        expected = [
            ["A", ["b A", "b B"]],
            ["B", ["b B", "b A"]],
            ["C", ["b A", "b B"]]
        ]

        actual = UniformRules(testing)
        self.assertEqual(expected, actual, "UniformRules can't do partly uniformed tasks")

    def test_rules_already_uniformed(self):
        testing = [
            ["A", ["b A", "b B"]],
            ["B", ["b B", "b A"]],
            ["C", ["b A", "b B"]]
        ]

        expected = [
            ["A", ["b A", "b B"]],
            ["B", ["b B", "b A"]],
            ["C", ["b A", "b B"]]
        ]

        actual = UniformRules(testing)
        self.assertEqual(expected, actual, "UniformRules badly processed already uniformed rules")


class Test_RemoveLeftRecursion(unittest.TestCase):

    def test_no_recursion(self):
        testing = [
            ["A", ["b A", "b B"]],
            ["B", ["b A", "b B"]],
            ["C", ["b A", "b B"]]
        ]

        expected = [
            ["A", ["b A", "b B"]],
            ["B", ["b A", "b B"]],
            ["C", ["b A", "b B"]]
        ]

        actual = RemoveLeftRecursion(testing, "LR")
        self.assertEqual(expected, actual, "RemoveLeftRecursion processed non recursive rules")

    def test_easy_recursion(self):
        testing = [
            ["A", ["A b", "b B"]],
            ["B", ["b A", "b B"]],
            ["C", ["b A", "b B"]]
        ]

        expected = [
            ["A", ["b B LR1"]],
            ["LR1", ["b LR1"]],
            ["LR1", ["e"]],
            ["B", ["b A", "b B"]],
            ["C", ["b A", "b B"]]
        ]

        actual = RemoveLeftRecursion(testing, "LR")
        self.assertEqual(expected, actual, "RemoveLeftRecursion cant do simple recursion")

   

if __name__ == '__main__':
    unittest.main()

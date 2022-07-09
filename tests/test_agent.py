import environment.env as env
from qlearning.agent import Agent
import unittest
from random import seed
import numpy as np


class EnvironmentTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.agent = Agent()

    def test_learning_rate_getter(self):
        self.assertEqual(0.1, self.agent.learning_rate)

    def test_learning_rate_setter(self):
        test_value = 0.9
        self.agent.learning_rate = test_value
        self.assertEqual(test_value, self.agent.learning_rate)

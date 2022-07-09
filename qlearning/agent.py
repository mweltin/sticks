import numpy as np
import random
import environment.env as env
import rules.rules as rules
import argparse
from os.path import exists
import matplotlib.pyplot as plt


class Agent:

    def __init__(self):
        self._learning_rate = 0.1
        self.discount_rate = 0.99
        self.min_exploration_rate = 0.01
        self.exploration_decay_rate = 0.001
        self._q_table = self.init_empty_q_table()
        pass

    def init_empty_q_table(self):
        action_space_size = len(env.action_table)
        state_space_size = len(env.state_table)
        return np.zeros((state_space_size, action_space_size))

    def set_q_table(self, table):
        self._q_table = table

    def get_q_table(self):
        return self._q_table

    q_table = property(get_q_table, set_q_table)

    def set_learning_rate(self, rate):
        self._learning_rate = rate

    def get_learning_rate(self):
        return self._learning_rate

    learning_rate = property(get_learning_rate, set_learning_rate)

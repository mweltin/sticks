import numpy as np
import random
import environment.env as env
import rules.rules as rules
from utilities.utility import Utility
from agent.player import Player


"""
An Agent is a Player that can learn. 
"""
class Agent(Player):

    def __init__(self, name='name not set'):
        super().__init__(self, name)
        self.exploration_rate = 1
        self._learning_rate = 0.1
        self.discount_rate = 0.99
        self._min_exploration_rate = 0.01
        self._exploration_decay_rate = 0.001
        self._q_table = self.init_empty_q_table()
        self.state_table = env.state_table
        self._name = name
        self.player_index = 0
        self.rewards_current_episode = 0
        self.max_exploration_rate = 1
        self.win_counter = 0
        self.wins_per_freq = []
        self.win_record_freq = 500
        self._utility = Utility("../data/" + self._name)

    def init_empty_q_table(self):
        action_space_size = len(env.action_table)
        state_space_size = len(env.state_table)
        return np.zeros((state_space_size, action_space_size))

    def set_q_table(self, table):
        self._q_table = table

    def get_q_table(self):
        return self._q_table

    q_table = property(get_q_table, set_q_table)

    def set_utility(self, name ):
        del self._utility
        self._utility = Utility(name)

    def get_utility(self):
        return self._utility

    utility = property(get_utility, set_utility)

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    name = property(get_name, set_name)

    def set_player_index(self, player_index):
        self._player_index = player_index

    def get_player_index(self):
        return self._player_index

    player_index = property(get_player_index, set_player_index)

    def set_learning_rate(self, rate):
        self._learning_rate = rate

    def get_learning_rate(self):
        return self._learning_rate

    learning_rate = property(get_learning_rate, set_learning_rate)

    def get_action(self, state_index):
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > self.exploration_rate:
            action = env.nanargmax_unbiased(self._q_table[state_index])
        else:
            action = env.select_random_action(state_index, self.player_index)
        return action

    def update_q_table(self, state_idx, new_state_idx, reward, done, action):
        if not done:
            self._q_table[state_idx][action] = self._q_table[state_idx][action]  + self._learning_rate * (
                                                       reward + self.discount_rate * env.nanargmax_unbiased(
                                                   self._q_table[new_state_idx]) - self._q_table[state_idx][action] )
        else:
            """if we are done at this point the AI has won.  Winning states have no valid moves. Therefore
            the expression np.nanargmax(q_table[new_state_idx] results in a ValueError and the q_table does
            not get updated.  For the state (0,1)(0,4) it doesn't matter as there is only one move.  However
            (0,4),(0,1) there are two moves: split or right right.  Without this block, only the split move
            would get updated in the q_table"""
            self._q_table[state_idx][action] = self._q_table[state_idx][action] + \
                                               self._learning_rate * (reward + self.discount_rate)

        rules.update_redundant_states(env.state_table[state_idx], self._q_table[state_idx][action], action,
                                      self._q_table)
        self.rewards_current_episode += reward

    def take_turn(self, state_index, episode):
        action = self.get_action(state_index)
        new_state_idx, reward, done, info = env.step(state_index, self.player_index, action)
        self.update_q_table(state_index, new_state_idx, reward, done, action)
        self.exploration_rate = self._min_exploration_rate + (
                self.max_exploration_rate - self._min_exploration_rate) * np.exp(
            -self._exploration_decay_rate * episode)
        return new_state_idx, done

    def save_output(self, prefix=None):
        self._utility.save_output(self._q_table, prefix)

    def record_wins(self):
        self.wins_per_freq.append(self.win_counter)
        self.win_counter = 0

    def plot_it(self):
        self._utility.plot_it(self.wins_per_freq, self.win_record_freq)

    def save_it(self):
        self._utility.save_it(self.wins_per_freq)

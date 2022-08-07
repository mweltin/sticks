from agent.exceptions import *
import environment.env as env
import random


class Player:

    def __init__(self, q_table=None, threshold=None, player_index=None, name=None, strategy=None):
        self._threshold = threshold
        self._q_table = q_table
        self._player_index = player_index
        self._name = name
        self._strategy = strategy

    def  take_turn(self, state_idx):
        if self._strategy == 'strict':
            action = self.get_action(state_idx)
        elif self._strategy == 'random':
            action = self.get_random_action(state_idx)
        elif self._strategy == 'threshold':
            action = self.get_action_with_random_threshold(state_idx)
        else:
            raise StrategyNotDefined(' valid values are strict, random, or threshold')

        return env.step(state_idx, self._player_index, action)

    def get_action(self, state_idx):
        return env.nanargmax_unbiased(self._q_table[state_idx])

    def get_random_action(self, state_idx):
        return env.select_random_action(state_idx, self._player_index)

    def get_action_with_random_threshold(self, state_idx, threshold=None):
        if not threshold and not self._threshold:
            raise MissingThreshold(' value must be on the interval [0,1]')

        explore_value = random.uniform(0, 1)
        if explore_value > self._threshold:
            return env.nanargmax_unbiased(self._q_table[state_idx])
        else:
            return env.select_random_action(state_idx, self._player_index)

    """============ getters and setters ================"""

    def set_q_table(self, table):
        self._q_table = table

    def get_q_table(self):
        return self._q_table

    q_table = property(get_q_table, set_q_table)

    def set_threshold(self, value):
        if value <= 1 or value >= 0:
            self._threshold = value
        else:
            raise ThresholdOutOfRange

    def get_threshold(self):
        return self._threshold

    threshold = property(get_threshold, set_threshold)

    def set_player_index(self, value):
        if value == 1 or value == 0:
            self._player_index = value
        else:
            raise PlayerIndexOutOfRange('player 1 = 0  and player 2 = 1')

    def get_player_index(self):
        return self._player_index

    player_index = property(get_player_index, set_player_index)

    def set_name(self, value):
        self._name = str(value)

    def get_name(self):
        return self._name

    name = property(get_name, set_name)

from agent.player import Player
from os.path import exists
import numpy as np
import rules.rules as rules
import environment.env as env


class Battle:

    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.max_turns = max_turns = 25

    def battle(self):
        winner = 'Draw'
        done = None
        self.player_1.player_index = 0
        self.player_2.player_index = 1
        state_idx = env.reset()
        turns = 0

        while turns < self.max_turns and not done:
            (state_idx, reward, done, info) = self.player_1.take_turn(state_idx)
            if done:
                winner = self.player_1.name
                break
            (state_idx, reward, done, info) = self.player_2.take_turn(state_idx)
            if done:
                winner = self.player_2.name
                break

            turns += 1

        print('winner is ' + winner)
        return winner

    def load_q_table_from_file(path_file_name):
        file_exists = exists(path_file_name)
        if file_exists:
            data = np.genfromtxt(path_file_name, delimiter=',')
            return data
        else:
            return False

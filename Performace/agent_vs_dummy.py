from agent.player import Player
from os.path import exists
import numpy as np
import rules.rules as rules
import environment.env as env


def battle(player_1, player_2, max_turns):
    winner = 'Draw'
    done = None
    player_1.player_index = 0
    player_2.player_index = 1
    state_idx = env.reset()
    turns = 0

    while turns < max_turns and not done:
        (state_idx, reward, done, info) = player_1.take_turn(state_idx)
        if done:
            winner = player_1.name
            break
        (state_idx, reward, done, info) = player_2.take_turn(state_idx)
        if done:
            winner = player_2.name
            break

        turns += 1

    print('winner is ' + winner)


def load_q_table_from_file(path_file_name):
    file_exists = exists(path_file_name)
    if file_exists:
        data = np.genfromtxt(path_file_name, delimiter=',')
        return data
    else:
        return False


if __name__ == '__main__':
    q_table = load_q_table_from_file('../data/q_table.csv')
    qlearning_player = Player(q_table=q_table, name='q_learning', strategy='strict')
    dummy_player = Player(name='dummy', strategy='random')
    for i in range(100):
        battle(qlearning_player, dummy_player, 25)

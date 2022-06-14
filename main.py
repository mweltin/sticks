# play a game of sticks
import numpy as np
import environment.env as env
import rules.rules as rules
import random
from copy import deepcopy

random.seed(19)


def print_hands_to_console(state):
    print('your hand ' + str(state[1]))
    print('computer hand ' + str(state[0]))


def build_valid_move_string(valid_moves):
    ret_str = []
    if 0 in valid_moves:
        ret_str.append('0 = swap')
    if 1 in valid_moves:
        ret_str.append('1 = left to left')
    if 2 in valid_moves:
        ret_str.append('2 = left to right')
    if 3 in valid_moves:
        ret_str.append('3 = right to right')
    if 4 in valid_moves:
        ret_str.append('4 = right to left')

    return 'Pick a Move: ' + ' , '.join(ret_str)


def play_sticks():
    q_table = np.genfromtxt("data/q_table_max_reward.csv", delimiter=",")
    state_idx = env.reset()

    user_goes_first = input('Welcome to sticks. Would you like to go first? (y/n)')  # Press Ctrl+F8 to toggle the breakpoint.
    if user_goes_first == 'y':
        active_player_idx = 1
    else:
        active_player_idx = 0

    has_winner = None
    current_state = deepcopy(env.state_table[state_idx])
    while has_winner is None:
        print_hands_to_console(current_state)
        if active_player_idx == 1:
            valid_moves = rules.get_valid_actions(current_state, active_player_idx)
            action = input(build_valid_move_string(valid_moves))
            while int(action) not in valid_moves:
                if action not in valid_moves:
                    print(str(action)+": was not a valid move.")
                    action = input(build_valid_move_string(valid_moves))
            current_state = rules.take_turn(current_state, active_player_idx, env.action_table[int(action)])
            active_player_idx = 0
        else:
            action = np.nanargmax(q_table[state_idx])
            print('computer action:' + str(env.action_table[action]))
            current_state = rules.take_turn(current_state, active_player_idx, env.action_table[action])
            active_player_idx = 1

        state_idx = env.state_table.index(current_state)
        has_winner = rules.has_winner(current_state)

    if has_winner == env.Players.opponent:
        print("congratulations! you won!")

    if has_winner == env.Players.agent:
        print("Better luck next time.")

    exit(0)


if __name__ == '__main__':
    play_sticks()

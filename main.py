# play a game of sticks
import numpy as np
import environment.env as env
import rules.rules as rules
import random
from copy import deepcopy

random.seed(19)


def print_hands_to_console(state):
    # print('Your left hand: ' + str(state[1][0]) + ' Your right hand: ' + str(state[1][1]))
    # print('Computer\'s left hand: ' + str(state[0][0]) + ' Computer\'s right hand: ' + str(state[0][1]))
    print('your hand ' + str(state[1]))
    print('computer hand ' + str(state[0]))


def play_sticks():
    q_table = np.genfromtxt("qlearning/q_table.csv", delimiter=",")
    state_idx = env.reset()

    user_goes_first = input(
        f'Welcome to sticks. Would you like to go first? (y/n)')  # Press Ctrl+F8 to toggle the breakpoint.
    if user_goes_first == 'y':
        active_player_idx = 1
    else:
        active_player_idx = 0

    has_winner = None
    current_state = deepcopy(env.state_table[state_idx])
    while has_winner is None:
        print_hands_to_console(current_state)
        if active_player_idx == 1:
            action = input(
                f'Pick a Move:  0 = swap, 1 = left to left, 2 = left to right \n' + \
                '3 = right to right 4 = right to left \n ')
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

# play a game of sticks
import numpy as np
import environment.env as env
import rules.rules as rules
import random
from copy import deepcopy


def print_hands_to_console(state):
    print('opponent hand ' + str(state[1]))
    print('agent hand ' + str(state[0]))


def play_sticks():
    q_table_agent = np.genfromtxt("data/q_table_max_reward.csv", delimiter=",")
    q_table_opponent = np.genfromtxt("data/q_table_max_reward.csv", delimiter=",")
    state_idx = env.reset()
    move_counter = 0
    active_player_idx = 1 if random.uniform(0, 1) < 0.5 else 0

    if active_player_idx == 0:
        print("agent goes first")
    else:
        print('opponent goes first')

    has_winner = None
    current_state = deepcopy(env.state_table[state_idx])
    while has_winner is None:
        move_counter += 1
        print_hands_to_console(current_state)
        if active_player_idx == 1:
            valid_moves = rules.get_valid_actions(current_state, active_player_idx)
            action = env.nanargmax_unbiased(q_table_opponent[state_idx])
            # action = env.select_random_action(state_idx, env.Players.opponent)
            print('opponent action:' + str(env.action_table[action]))
            current_state = rules.take_turn(current_state, active_player_idx, env.action_table[int(action)])
            active_player_idx = 0
        else:
            action = env.nanargmax_unbiased(q_table_agent[state_idx])
            print('agent action:' + str(env.action_table[action]))
            current_state = rules.take_turn(current_state, active_player_idx, env.action_table[action])
            active_player_idx = 1

        state_idx = env.state_table.index(current_state)
        has_winner = rules.has_winner(current_state)

        if move_counter == 100 and has_winner is None:
            print("Draw after " + str(move_counter) + " moves")
            return

    if has_winner == env.Players.opponent:
        print("Opponent won in " + str(move_counter) + " moves")

    if has_winner == env.Players.agent:
        print("Agent won in " + str(move_counter) + " moves")

    exit(0)


if __name__ == '__main__':
    play_sticks()

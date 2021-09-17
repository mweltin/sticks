from enum import IntEnum
import random
import rules.rules as rules
from copy import deepcopy


def reset():
    return state_table.index([[1, 1], [1, 1]])


# redesign for test ability
def eliminate_invalid_actions(states, q_table):
    for idx, array in enumerate(states):
        valid_actions = rules.get_valid_actions(array, 0)
        for atidx, val in enumerate(q_table[idx]):
            if atidx not in valid_actions:
                q_table[idx][atidx] = None


def select_random_action(state_index, player_index):
    possible_action = rules.get_valid_actions(state_table[state_index], player_index)
    if len(possible_action) == 1:
        return possible_action[0]
    action_index = random.randint(0, len(possible_action) - 1)
    return possible_action[action_index]


# these are only from the perspective of the agent
def get_reward(state):
    if rules.has_winner(state) == Players.agent:
        return 100
    if rules.has_winner(state) == Players.opponent:
        return -100
    if will_lose_next_step(state):
        return -50
    if will_win_in_two_steps(state):
        return 50

    return -1


def will_lose_next_step(state):
    state_copy = deepcopy(state)
    state_copy[Players.agent].sort()
    if state_copy[Players.agent][Hands.left] == 0:
        if state_copy[Players.agent][Hands.right] + state_copy[Players.opponent][Hands.left] == 5 or \
                state_copy[Players.agent][Hands.right] + state_copy[Players.opponent][Hands.right] == 5:
            return True
    return False


def will_win_in_two_steps(state):
    state_copy = deepcopy(state)
    state_copy[Players.agent].sort()
    state_copy[Players.opponent].sort()
    if state_copy[Players.agent][Hands.left] == 0 == state_copy[Players.opponent][Hands.left]:
        if state_copy[Players.agent][Hands.right] + (2 * state_copy[Players.opponent][Hands.right]) == 5:
            return True
    return False


# return a list of [new_state_idx, reward, done, info]
def step(state_idx, player_idx, action_idx):
    done = False
    action = action_table[action_idx]
    state = deepcopy(state_table[state_idx])
    new_state = rules.take_turn(state, player_idx, action)
    if rules.has_winner(new_state) is not None:
        done = True
    reward = get_reward(new_state)
    return [state_table.index(new_state), reward, done, {'info': None}]


state_table = []
for i in range(5):
    for x in range(5):
        for y in range(5):
            for z in range(5):
                state_table.append([[i, x], [y, z]])
# first state [[0,0],[0,0]] is not a valid state so get rid of it
state_table.pop(0)


class Players(IntEnum):
    agent = 0
    opponent = 1


class Hands(IntEnum):
    left = 0
    right = 1


class Actions(IntEnum):
    LEFT = 0
    RIGHT = 1
    SWAP = 2


# A player can perform one of these actions swap,
# attack with left hand to opponents right hand
# attack with left hand to opponents left hand
# attack with right hand to opponents left hand
# attack with right hand to opponents right hand
action_table = [
    [Actions.SWAP],
    [Actions.LEFT, Actions.LEFT],
    [Actions.LEFT, Actions.RIGHT],
    [Actions.RIGHT, Actions.RIGHT],
    [Actions.RIGHT, Actions.LEFT]
]

if __name__ == '__main__':
    print("did you mean to import the environment file")

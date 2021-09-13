from enum import IntEnum
import random
import rules.rules as rules
from copy import deepcopy

state_table = []
for i in range(5):
    for x in range(5):
        for y in range(5):
            for z in range(5):
                state_table.append([[i, x], [y, z]])
# first state [[0,0],[0,0]] is not a valid state so get rid of it
state_table.pop()


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


def reset():
    return 156  # starting state [[1,1],[1,1]]


def select_random_action(state_index, player_index):
    possible_action = rules.get_valid_actions(state_table[state_index], player_index)
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


if __name__ == '__main__':
    main()

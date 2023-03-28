from enum import IntEnum
import random
import rules.rules as rules
from copy import deepcopy
import numpy as np
from random import randint


def reset():
    """
    reset: Bring the game back to the initial starting conditions i.e. Each player with one finger out on both hands

    :return: 2D number array [ [AI left, AI right ], [human left, human right]  ]
    """
    return state_table.index([[1, 1], [1, 1]])


def state_to_tensor(state_idx):
    """ used as an input into a DQN """
    flat_list = [num for sublist in state_table[state_idx] for num in sublist]
    return np.array(flat_list)


def eliminate_invalid_actions(state, q_table):
    """
    eliminate_invalid_actions: For certain states certain actions are not allowed.  The 'swap' action for example is not
    allowed when both hands have a value, or one hand is zero but the other hand has an odd number of fingers.  This
    function will set the value of each invalid action in the q_table to NAN.  This will ensure that when the
    Q-learning algorithm is deciding which action to take it will avoid invalid actions.

    :param state: The state_table a 2D array of all possible states (i.e. valid combinations of player hands)
    :param q_table: A matrix (2d python list) with dimensions Stats X Actions
    :return:
    """
    for idx, array in enumerate(state):
        valid_actions = rules.get_valid_actions(array, 0)
        for atidx, val in enumerate(q_table[idx]):
            if atidx not in valid_actions:
                q_table[idx][atidx] = None


def select_random_action(state_index, player_index):
    """
    select_random_action For a give state and player select a random action to take.  Used primarily by the AI to
    explore the solution space.

    :param state_index: Current state of the game (i.e. the fingers on each hand of each player)
    :param player_index: The active player (0 human, 1 AI)
    :return: a randomly selected valid action
    """
    possible_action = rules.get_valid_actions(state_table[state_index], player_index)
    if len(possible_action) == 1:
        return possible_action[0]
    action_index = random.randint(0, len(possible_action) - 1)
    return possible_action[action_index]


def get_reward(state):
    """
    get_reward: The reward system is used by the AI to help it learn.  The Belman equation is trying to maximize it's
    reward over time.  This function is one of the major tuning parameters for the algorithm.  It defines an
    incentive structure for the QLeaning algorithm.  This is a very simple structure, if it wins it gets 100 points, if
    looses it gets -100 points.  If it can win in two steps it gets 50 points and if couldn't lose in the next turn
    it looses 50 points.  All other states have a 1 point penalty.

    :param state: Current state of the game (i.e. the fingers on each hand of each player)
    :return: How much the algorithm is rewarded for the the state that it is in.
    """
    if rules.has_winner(state) == Players.agent:
        return 1
    if rules.has_winner(state) == Players.opponent:
        return -1
    if will_lose_next_step(state):
        return -0.5
    if will_win_in_two_steps(state):
        return 0.5

    return 0


def will_lose_next_step(state):
    """
    will_lose_next_step: Used by the reward system, this function will check to see if the AI could potentially
    lose when its opponent takes it next turn.

    :param state: Current state of the game (i.e. the fingers on each hand of each player)
    :return: If the AI already has zero in one hand and either of the opponents hands could be used to
    knock out the AI this will return True, False otherwise.
    """
    state_copy = deepcopy(state)
    state_copy[Players.agent].sort()
    if state_copy[Players.agent][Hands.left] == 0:
        if state_copy[Players.agent][Hands.right] + state_copy[Players.opponent][Hands.left] == 5 or \
                state_copy[Players.agent][Hands.right] + state_copy[Players.opponent][Hands.right] == 5:
            return True
    return False


def will_win_in_two_steps(state):
    """
    will_win_in_two_steps: The reward system is always done from the perspective of the AI.  This function is used
    by the reward system to give some extra incentive if the AI comes close to a win.

    :param state: Current state of the game (i.e. the fingers on each hand of each player)
    :return: If the AI gets to a state where it can win on its next move (i.e. the next move it takes after the human
    has had a turn) return True, False otherwise.
    """
    state_copy = deepcopy(state)
    state_copy[Players.agent].sort()
    state_copy[Players.opponent].sort()
    if state_copy[Players.agent][Hands.left] == 0 == state_copy[Players.opponent][Hands.left]:
        if (state_copy[Players.agent][Hands.right] + (2 * state_copy[Players.opponent][Hands.right])) % 5 == 0:
            return True
    return False


# return a list of [new_state_idx, reward, done, info]
def step(state_idx, player_idx, action_idx):
    """
    step: Take a step forward in the game.  Essentially this does some data wrangling in order to call the take_turn
    function in the rules library.

    :param state_idx: Index in the state_table for the current state of the game.
    :param player_idx: 0 = human, 1 = AI
    :param action_idx: The index in the action table the player will take
    :return: a list containing the new state index after the action was taken, the associated reward with that action,
    if the game has a winner, and an object called info which is not currently implemented.
    """
    done = False
    action = action_table[action_idx]
    state = deepcopy(state_table[state_idx])
    new_state = rules.take_turn(state, player_idx, action)
    if rules.has_winner(new_state) is not None:
        done = True
    reward = get_reward(new_state)
    return [state_table.index(new_state), reward, done, {'info': None}]


def nanargmax_unbiased(action_array):
    """
    pick_max: The np.nanargmax introduces a selection bias.  If two or more elements have the same value the
    np.nanargmax will always return the first value.

    :param action_array the array of possible actions i.e. a row in the q_table
    :return: the index of the largest value in action_array.  If there are two or more max values return a
    index at random from the set of indexes that hold a max value.
    """
    index = np.nanargmax(action_array)
    val = action_array[index]
    if action_array[action_array == val].shape[0] > 1:
        index_list = []
        for idx, value in enumerate(action_array):
            if value == val:
                index_list.append(idx)
        index = index_list[randint(0, len(index_list) - 1)]

    return index


"""
Generate all states, even invalid states.  These will be cleaned up later.
"""
state_table = []
for i in range(5):
    for x in range(5):
        for y in range(5):
            for z in range(5):
                state_table.append([[i, x], [y, z]])
"""
[0,0],[0,0]] is not a valid state so get rid of it
"""
state_table.pop(0)

"""
Define Players Enum, helps make main code easier to read
"""


class Players(IntEnum):
    agent = 0
    opponent = 1


"""
Define Hands Enum, helps make main code easier to read
"""


class Hands(IntEnum):
    left = 0
    right = 1


"""
Define Actions Enum, helps make main code easier to read
"""


class Actions(IntEnum):
    LEFT = 0
    RIGHT = 1
    SWAP = 2


"""
Generate a list of all possible actions using the Enums defined above to make the main code easier to read
A player can perform one of these actions swap,
Attack with left hand to opponents right hand
Attack with left hand to opponents left hand
Attack with right hand to opponents left hand
Attack with right hand to opponents right hand
"""
action_table = [
    [Actions.SWAP],
    [Actions.LEFT, Actions.LEFT],
    [Actions.LEFT, Actions.RIGHT],
    [Actions.RIGHT, Actions.RIGHT],
    [Actions.RIGHT, Actions.LEFT]
]

"""
current state = [[a,b],[c,d]]
from the action_table index 0 we would swap and for each redundant row the action index would not change.
from the action_table index 1 would imply that a would tap c
When looking at redundant state [[b,a],[c,d]] the action index for a tap c would be 4
The table below maps the state action index to the appropriate redundant state action index.
The index of the redundant_state_action_index_mapping mathes the action_table index id 
redundant_state_action_index_mapping[0] -> swap 
redundant_state_action_index_mapping[2] -> left to right
"""
redundant_state_action_index_mapping = [
    {'[b,a],[c,d]': 0, '[a,b],[d,c]': 0, '[b,c],[d,c]': 0},
    {'[b,a],[c,d]': 4, '[a,b],[d,c]': 2, '[b,c],[d,c]': 3},
    {'[b,a],[c,d]': 3, '[a,b],[d,c]': 1, '[b,c],[d,c]': 4},
    {'[b,a],[c,d]': 2, '[a,b],[d,c]': 4, '[b,c],[d,c]': 1},
    {'[b,a],[c,d]': 1, '[a,b],[d,c]': 3, '[b,c],[d,c]': 2},
]

if __name__ == '__main__':
    print("did you mean to import the environment file")

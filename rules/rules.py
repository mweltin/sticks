# rules the govern the game of sticks
# see https://en.wikipedia.org/wiki/Chopsticks_(hand_game)
import environment.env as env
from copy import deepcopy


# Be careful using this Players.agent is 0 and hence "falsy" when evaluating the return value of has_winner
# look for specific values not truthy or falsy values.
def has_winner(state):
    # in is the current state of the game two dimension array of two integers each
    if state[env.Players.agent][env.Hands.left] == 0 and state[env.Players.agent][env.Hands.right] == 0:
        return env.Players.opponent

    if state[env.Players.opponent][env.Hands.left] == 0 and state[env.Players.opponent][env.Hands.right] == 0:
        return env.Players.agent

    return None


# inputs: an array with two integer elements
def can_swap(player_state):
    # a player can only swap if one hand is at zero and the other is even
    val = deepcopy(player_state)  # make a copy of player_state object reference
    val.sort()
    if val[0] == 0 and val[1] != 0 and not val[1] % 2:
        return True

    return False


def swap(state):
    # perform the swap action.
    state.sort()
    return [state[1] / 2, state[1] / 2]


def get_opponent_player_index(active_player_index):
    if active_player_index:
        return 0
    return 1


# state 2 d array enumerating each Players env.Hands
# index of the active player
def take_turn(state, active_player_index, action):
    take_swap = False
    opponent_player_index = None
    opponent_hand = None
    active_player_hand = None

    if action[0] == env.Actions.SWAP:
        take_swap = True
    else:
        opponent_player_index = get_opponent_player_index(active_player_index)
        if action[0] == env.Hands.left:
            active_player_hand = 0
        else:
            active_player_hand = 1

        if action[1] == env.Hands.left:
            opponent_hand = 0
        else:
            opponent_hand = 1

    if take_swap:
        state[active_player_index] = swap(state[active_player_index])
    else:
        state[opponent_player_index][opponent_hand] = (state[opponent_player_index][opponent_hand] + \
                                                       state[active_player_index][active_player_hand]) % 5
    return state





# state = 2d array of representing the state of the game
# player_index indicates who is the active player i.e. the one swapping or attacking
# returns a dictionary of possible moves
def get_valid_actions(state, active_player):
    ret_val = []
    if can_swap(state[active_player]):
        ret_val.append(env.action_table.index([env.Actions.SWAP]))
    opponent_player_index = get_opponent_player_index(active_player)
    if state[active_player][1] > 0 and state[opponent_player_index][1] > 0:
        ret_val.append(env.action_table.index([env.Actions.RIGHT, env.Actions.RIGHT]))
    if state[active_player][1] > 0 and state[opponent_player_index][0] > 0:
        ret_val.append(env.action_table.index([env.Actions.RIGHT, env.Actions.LEFT]))
    if state[active_player][0] > 0 and state[opponent_player_index][1] > 0:
        ret_val.append(env.action_table.index([env.Actions.LEFT, env.Actions.RIGHT]))
    if state[active_player][0] > 0 and state[opponent_player_index][0] > 0:
        ret_val.append(env.action_table.index([env.Actions.LEFT, env.Actions.LEFT]))
    return ret_val


if __name__ == '__main__':
    print("did you mean to import the rules file")

# rules the govern the game of sticks
# see https://en.wikipedia.org/wiki/Chopsticks_(hand_game)

def is_done(state):
    # in is the current state of the game two dimension array of two integers each
    if state[0][0] == 0 and state[0][1] == 0:
        return 1

    if state[1][0] == 0 and state[1][1] == 0:
        return 2

    return 0


# inputs: an array with two integer elements
def can_swap(player_state):
    # a player can only swap if one hand is at zero and the other is even
    val = player_state[:]  # make a copy of player_state object reference
    val.sort()
    if val[0] == 0 and not val[1] % 2:
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


# state 2 d array enumerating each players hands
# index of the active player
def take_turn(state, active_player_index, active_player_hand, opponent_hand, take_swap_action=False):
    if take_swap_action:
        state[active_player_index] = swap(state[active_player_index])
    else:
        opponent_player_index = get_opponent_player_index(active_player_index)
        state[opponent_player_index][opponent_hand] = (state[opponent_player_index][opponent_hand] + \
                                                       state[active_player_index][active_player_hand]) % 5

    return state


# state = 2d array of representing the state of the game
# player_index indicates who is the active player i.e. the one swapping or attacking
# returns a dictionary of possible moves
def get_valid_actions(state, active_player):
    ret_val = []
    if can_swap(state[active_player]):
        ret_val.append("swap")
    opponent_player_index = get_opponent_player_index(active_player)
    if state[active_player][1] > 0 and state[opponent_player_index][1] > 0:
        ret_val.append("right_right")
    if state[active_player][1] > 0 and state[opponent_player_index][0] > 0:
        ret_val.append("right_left")
    if state[active_player][0] > 0 and state[opponent_player_index][1] > 0:
        ret_val.append("left_right")
    if state[active_player][0] > 0 and state[opponent_player_index][0] > 0:
        ret_val.append("left_left")
    return ret_val

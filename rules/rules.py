# rules the govern the game of sticks
# see https://en.wikipedia.org/wiki/Chopsticks_(hand_game)

def is_done(state):
    # in is the current state of the game two dimension array of two integers each
    if state[0][0] == 0 and state[0][1] == 0:
        return 1

    if state[1][0] == 0 and state[1][1] == 0:
        return 2

    return 0


def can_swap(state):
    # a player can only swap if one hand is at zero and the other is even
    state.sort()
    if state[0] == 0 and not state[1] % 2:
        return True

    return False


def swap(state):
    # perform the swap action.
    state.sort()
    return [state[1] / 2, state[1] / 2]


def take_turn(state, active_player, active_player_hand, opponent_hand, take_swap_action=False):
    if take_swap_action:
        state[active_player] = swap(state[active_player])
    else:
        state[not active_player][opponent_hand] = state[not active_player][opponent_hand] + state[active_player][
            active_player_hand] % 5

    return state

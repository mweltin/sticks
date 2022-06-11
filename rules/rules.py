import environment.env as env
from copy import deepcopy


def has_winner(state):
    """
    has_winner: Determine if someone has won the game. Be careful using this Players.agent is 0 and hence "falsy" when
    evaluating the return value of has_winner look for specific values not truthy or falsy values.

    :param state: Current state of the game (i.e. the fingers on each hand of each player).
    :return: 0 if IA has won, 1 if the human player has won.  (rules.Players Enum return value)
    """
    if state[env.Players.agent][env.Hands.left] == 0 and state[env.Players.agent][env.Hands.right] == 0:
        return env.Players.opponent

    if state[env.Players.opponent][env.Hands.left] == 0 and state[env.Players.opponent][env.Hands.right] == 0:
        return env.Players.agent

    return None


def can_swap(player_state):
    """
    can_swap given a single player's state, this is used to decide if a swap is a legal move for them. If a player has
    zero fingers on one hand and an even number of fingers on the other they are allowed to perform a swap.

    :param player_state: 1D array (list) of the player that is being evaluated.
    :return: True if the play can swap or False otherwise.
    """
    # a player can only swap if one hand is at zero and the other is even
    val = deepcopy(player_state)  # make a copy of player_state object reference
    val.sort()
    if val[0] == 0 and val[1] != 0 and not val[1] % 2:
        return True

    return False


def swap(state):
    """
    swap: Perform the swap action.

    :param state: 1D array (list) of the current players hand.
    :return: new 1D array after performing the swap
    """
    state.sort()
    return [int(state[1] / 2), int(state[1] / 2)]


def get_opponent_player_index(active_player_index):
    """
    get_opponent_player_index: Gets the env.Players Enum value of the non active player.

    :param active_player_index: env.Players Enum of the active player
    :return: The env.Players Enum of the inactive player.
    """
    if active_player_index:
        return 0
    return 1


# state 2 d array enumerating each Players env.Hands
# index of the active player
def take_turn(state, active_player_index, action):
    """
    take_turn: This function updates the either the players hand in the case of the swap or the opponents hand
    in the case of a non-swap action.

    :param state: Current state of the game (i.e. the fingers on each hand of each player).
    :param active_player_index: env.Players Enum of the active whoe is taking their turn.
    :param action: A list of env.Actions Enums indicating the action to take.  The list will have one element in
        the case of a swap, or two elements to indicate which player hand is acting on which hand of their opponent.
    :return: The new state of the active player in the case of a swap, or the new state fo the opponent in the
        case of a non-swap action.
    """
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
        state[opponent_player_index][opponent_hand] = (state[opponent_player_index][opponent_hand] +
                                                       state[active_player_index][active_player_hand]) % 5
    return state


def get_valid_actions(state, active_player):
    """
    get_valid_actions: Some actions are invalid depending on the state of the game.  For example a player can not use
        a hand that has zero fingers to tap an opponents hand, of perform a swap action if their non zero hand has
        and odd number of fingers.
    :param state: Current state of the game (i.e. the fingers on each hand of each player).
    :param active_player: env.Players Enum of the active player 0 for AI, 1 for human
    :return: A list of action_table indices for each valid action that the active_player can take.
    """
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


def update_redundant_states(state, value, action_index, q_table):
    a = state[0][0]
    b = state[0][1]
    c = state[1][0]
    d = state[1][1]

    redundant_states = get_redundant_states(state)

    if [[b, a], [c, d]] in redundant_states:
        states_row_index = env.state_table.index([[b, a], [c, d]])
        q_table[states_row_index][env.redundant_state_action_index_mapping[action_index]['[b,a],[c,d]']] = value

    if [[a, b], [d, c]] in redundant_states:
        states_row_index = env.state_table.index([[a, b], [d, c]])
        q_table[states_row_index][env.redundant_state_action_index_mapping[action_index]['[a,b],[d,c]']] = value

    if [[b, a], [d, c]] in redundant_states:
        states_row_index = env.state_table.index([[b, a], [d, c]])
        q_table[states_row_index][env.redundant_state_action_index_mapping[action_index]['[b,c],[d,c]']] = value

    return q_table


def get_redundant_states(state):
    redundant_states = []
    a = state[0][0]
    b = state[0][1]
    c = state[1][0]
    d = state[1][1]
    if a == b and c == d:
        """both sides are symetrical therefore 0 redundant states"""
        pass

    if (a != b and c == d) or (a == b and c != d):
        """ only one side is asymetrical therefore there exists only 1 redundant state"""
        if a == b:
            redundant_states.append([[a, b], [d, c]])
        else:
            redundant_states.append([[b, a], [c, d]])

    if a != b and c != d:
        redundant_states.append([[b, a], [c, d]])
        redundant_states.append([[a, b], [d, c]])
        redundant_states.append([[b, a], [d, c]])

    return redundant_states


if __name__ == '__main__':
    print("did you mean to import the rules file")

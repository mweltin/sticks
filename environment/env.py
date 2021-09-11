from enum import IntEnum
import rules.rules as rules

state_table = []
for i in range(5):
    for x in range(5):
        for y in range(5):
            for z in range(5):
                state_table.append([[i, x], [y, z]])
# first state [[0,0],[0,0]] is not a valid state so get rid of it
state_table.pop()


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
action_space = len(action_table)  # 5
state_space = len(state_table)  # 624


def reset():
    return 156 # starting state [[1,1],[1,1]]


def random_action(state_index):
    can_swap = rules.can_swap(state_table[state_index])


if __name__ == '__main__':
    main()

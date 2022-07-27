import os
import numpy as np
from agent.player import Player
from agent.battle import Battle

number_of_training_runs = 2

results = {
    'qlearning':
        {
            'go first': [],
            'go second': []
        },
    'wolf': {
        'go first': [],
        'go second': []
    },
    'dual_1': {
        'go first': [],
        'go second': []
    },
    'dual_2': {
        'go first': [],
        'go second': []
    },
}
## q_learner vs dummy
for i in range(number_of_training_runs):
    os.system("python ../qlearning/qlearning.py --skip_plot=True")
    q_table = np.genfromtxt('../data/q_table.csv', delimiter=',')

    qplayer = Player(q_table=q_table, player_index=0, name='q_player', strategy='strict')
    dummy = Player(name='dummy', player_index=1, strategy='random')

    battle = Battle(qplayer, dummy)
    winner = battle.battle()

    results['qlearning']['go first'].append(winner)

    qplayer = Player(q_table=q_table, player_index=1, name='q_player', strategy='strict')
    dummy = Player(name='dummy', player_index=0, strategy='random')

    battle2 = Battle(dummy, qplayer)
    winner = battle2.battle()

    results['qlearning']['go second'].append(winner)

for i in range(number_of_training_runs):
    os.system("python ../qlearning/wolf.py --skip_plot=True")
    q_table = np.genfromtxt('../data/q_table.csv', delimiter=',')

    wolf = Player(q_table=q_table, player_index=0, name='wolf', strategy='strict')
    dummy = Player(name='dummy', player_index=1, strategy='random')

    battle = Battle(wolf, dummy)
    winner = battle.battle()
    results['wolf']['go first'].append(winner)

    wolf = Player(q_table=q_table, player_index=1, name='wolf', strategy='strict')
    dummy = Player(name='dummy', player_index=0, strategy='random')

    battle2 = Battle(dummy, wolf)
    winner = battle2.battle()
    results['wolf']['go second'].append(winner)

for i in range(number_of_training_runs):
    os.system("python ../qlearning/dual_agent.py --skip_plot=True")
    q_table_1 = np.genfromtxt('../data/agent_1.csv', delimiter=',')
    q_table_2 = np.genfromtxt('../data/agent_2.csv', delimiter=',')

    agent_1 = Player(q_table=q_table_1, player_index=0, name='agent_1', strategy='strict')
    agent_2 = Player(q_table=q_table_2, player_index=0, name='agent_2', strategy='strict')
    dummy = Player(name='dummy', player_index=1, strategy='random')

    battle = Battle(agent_1, dummy)
    winner = battle.battle()
    results['dual_1']['go first'].append(winner)

    battle = Battle(agent_2, dummy)
    winner = battle.battle()
    results['dual_1']['go second'].append(winner)

    agent_1 = Player(q_table=q_table_1, player_index=1, name='agent_1', strategy='strict')
    agent_2 = Player(q_table=q_table_2, player_index=1, name='agent_2', strategy='strict')
    dummy = Player(name='dummy', player_index=0, strategy='random')

    battle = Battle(dummy, agent_1)
    winner = battle.battle()
    results['dual_2']['go first'].append(winner)

    battle = Battle(dummy, agent_2)
    winner = battle.battle()
    results['dual_2']['go second'].append(winner)
pass
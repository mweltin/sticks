import os
import numpy as np
from agent.player import Player
from agent.battle import Battle

number_of_training_runs = 2
## q_learner vs dummy
for i in range(number_of_training_runs):
    os.system("python ../qlearning/qlearning.py --skip_plot=True")
    q_table =  np.genfromtxt('../data/q_table.csv', delimiter=',')

    qplayer = Player(q_table=q_table, player_index=0, name='q_player', strategy='strict')
    dummy = Player(name='dummy', player_index=1, strategy='random')

    battle = Battle(qplayer, dummy)
    winner = battle.battle()

    qplayer = Player(q_table=q_table, player_index=1, name='q_player', strategy='strict')
    dummy = Player(name='dummy', player_index=0, strategy='random')

    battle2 = Battle(dummy, qplayer)
    winner = battle2.battle()

results = {}

for i in range(2):
    os.system("python ../qlearning/wolf.py --skip_plot=True")
    q_table =  np.genfromtxt('../data/q_table.csv', delimiter=',')

    wolf = Player(q_table=q_table, player_index=0, name='wolf', strategy='strict')
    dummy = Player(name='dummy', player_index=1, strategy='random')

    battle = Battle(wolf, dummy)
    winner = battle.battle()

    wolf = Player(q_table=q_table, player_index=1, name='wolf', strategy='strict')
    dummy = Player(name='dummy', player_index=0, strategy='random')

    battle2 = Battle(dummy, wolf)
    winner = battle2.battle()




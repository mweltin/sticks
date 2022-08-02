import os
import numpy as np
from agent.player import Player
from agent.battle import Battle

number_of_training_runs = 100

results = {
    'qlearning':
        {
            'vs_dummy':
                {
                    'go_first': [],
                    'go_second': []
                },
            'vs_wolf':
                {
                    'go_first': [],
                    'go_second': []
                },
            'vs_dual_1':
                {
                    'go_first': [],
                    'go_second': []
                },
            'vs_dual_2':
                {
                    'go_first': [],
                    'go_second': []
                }
        },
    'wolf':
        {
            'vs_dummy':
                {
                    'go_first': [],
                    'go_second': []
                },
            'vs_dual_1':
                {
                    'go_first': [],
                    'go_second': []
                },
            'vs_dual_2':
                {
                    'go_first': [],
                    'go_second': []
                }
        },
    'dual_1':
        {
            'vs_dummy':
                {
                    'go_first': [],
                    'go_second': []
                },
        },
    'dual_2':
        {
            'vs_dummy':
                {
                    'go_first': [],
                    'go_second': []
                },
        }
}

for i in range(number_of_training_runs):
    # train with the three different algorithms
    os.system("python ../qlearning/qlearning.py --skip_plot=True")
    os.system("python ../qlearning/wolf.py --skip_plot=True")
    os.system("python ../qlearning/dual_agent.py --skip_plot=True")

    qlearning_q_table = np.genfromtxt('../data/qlearning/q_table.csv', delimiter=',')
    wolf_q_table = np.genfromtxt('../data/wolf/q_table.csv', delimiter=',')
    dual_1_q_table = np.genfromtxt('../data/dual/agent_1/q_table.csv', delimiter=',')
    dual_2_q_table = np.genfromtxt('../data/dual/agent_2/q_table.csv', delimiter=',')

    q_player = Player(q_table=qlearning_q_table, name='q_player', strategy='strict')
    wolf_player = Player(q_table=wolf_q_table, name='q_player', strategy='strict')
    dual_1_player = Player(q_table=dual_1_q_table, name='q_player', strategy='strict')
    dual_2_player = Player(q_table=dual_2_q_table, name='q_player', strategy='strict')
    dummy_player = Player(name='dummy', strategy='random')

    # q_learning vs dummy
    battle = Battle(q_player, dummy_player)
    winner = battle.battle()
    results['qlearning']['vs_dummy']['go_first'].append(winner)

    battle = Battle(dummy_player, q_player)
    winner = battle.battle()
    results['qlearning']['vs_dummy']['go_second'].append(winner)

    # wolf vs dummy
    battle = Battle(wolf_player, dummy_player)
    winner = battle.battle()
    results['wolf']['vs_dummy']['go_first'].append(winner)

    battle = Battle(dummy_player, wolf_player)
    winner = battle.battle()
    results['wolf']['vs_dummy']['go_second'].append(winner)

    # d ual 1 vs dummy
    battle = Battle(dual_1_player, dummy_player)
    winner = battle.battle()
    results['dual_1']['vs_dummy']['go_first'].append(winner)

    battle = Battle(dummy_player, dual_1_player)
    winner = battle.battle()
    results['dual_1']['vs_dummy']['go_second'].append(winner)

    # dual 2 vs dummy
    battle = Battle(dual_2_player, dummy_player)
    winner = battle.battle()
    results['dual_2']['vs_dummy']['go_first'].append(winner)

    battle = Battle(dummy_player, dual_2_player)
    winner = battle.battle()
    results['dual_2']['vs_dummy']['go_second'].append(winner)

    # qlearning vs wolf
    battle = Battle(q_player, wolf_player)
    winner = battle.battle()
    results['qlearning']['vs_wolf']['go_first'].append(winner)

    # wolf vs dummy
    battle = Battle(wolf_player, q_player)
    winner = battle.battle()
    results['qlearning']['vs_wolf']['go_second'].append(winner)

# save results  naming convention player 1 vs player 2,  player 1 always went first
# qlearning vs dummy
np.savetxt("../data/qlearning/battle_data/gl_vs_dummy_results.csv", results['qlearning']['vs_dummy']['go_first'],
           delimiter=", ", fmt='% s', header='ql vs dummy')
# dummy vs qlearning
np.savetxt("../data/qlearning/battle_data/dummy_vs_ql_results.csv", results['qlearning']['vs_dummy']['go_second'],
           delimiter=", ", fmt='% s', header='ql vs dummy')
# qlearning vs wolf
np.savetxt("../data/qlearning/battle_data/ql_vs_wolf_results.csv", results['qlearning']['vs_wolf']['go_first'],
           delimiter=", ", fmt='% s', header='ql vs wolf')
# wolf vs qlearning
np.savetxt("../data/qlearning/battle_data/wolf_vs_ql_results.csv", results['qlearning']['vs_wolf']['go_second'],
           delimiter=", ", fmt='% s', header='wolf vs ql')
# qlearning vs dual_1
np.savetxt("../data/qlearning/battle_data/ql_vs_dual_1_results.csv", results['qlearning']['vs_dual_1']['go_first'],
           delimiter=", ", fmt='% s', header='ql vs dual_1')
# dual_1 vs qlearning
np.savetxt("../data/qlearning/battle_data/dual_1_vs_ql_results.csv", results['qlearning']['vs_dual_1']['go_second'],
           delimiter=", ", fmt='% s', header='dual_1 vs ql')
# qlearning vs dual_2
np.savetxt("../data/qlearning/battle_data/ql_vs_dual_2_results.csv", results['qlearning']['vs_dual_2']['go_first'],
           delimiter=", ", fmt='% s', header='ql vs dual_2')
# dual_2 vs qlearning
np.savetxt("../data/qlearning/battle_data/dual_2_vs_ql_results.csv", results['qlearning']['vs_dual_2']['go_second'],
           delimiter=", ", fmt='% s', header='dual_2 vs ql')
# wolf vs dummy
np.savetxt("../data/wolf/battle_data/wolf_vs_dummy_results.csv", results['wolf']['vs_dummy']['go_first'],
           delimiter=", ", fmt='% s', header='wolf vs dummy')
# dummy vs wolf
np.savetxt("../data/wolf/battle_data/dummy_vs_wolf_results.csv", results['wolf']['vs_dummy']['go_second'],
           delimiter=", ", fmt='% s', header='dummy vs wolf')
# wolf vs dual_1
np.savetxt("../data/wolf/battle_data/wolf_vs_dual_1_results.csv", results['wolf']['vs_dual_1']['go_first'],
           delimiter=", ", fmt='% s', header='wolf vs dual_1')
# dual_1 vs wolf
np.savetxt("../data/wolf/battle_data/dual_1_vs_wolf_results.csv", results['wolf']['vs_dual_1']['go_second'],
           delimiter=", ", fmt='% s', header='dual_1 vs wolf')
# wolf vs dual_2
np.savetxt("../data/wolf/battle_data/wolf_vs_dual_2_results.csv", results['wolf']['vs_dual_2']['go_first'],
           delimiter=", ", fmt='% s', header='wolf vs dual_2')
# dual_2 vs wolf
np.savetxt("../data/wolf/battle_data/dual_2_vs_wolf_results.csv", results['wolf']['vs_dual_2']['go_second'],
           delimiter=", ", fmt='% s', header='dual_2 vs wolf')
# dual_1 vs dummy
np.savetxt("../data/dual/agent_1/battle_data/dual_1_vs_dummy_results.csv", results['dual_1']['vs_dummy']['go_first'],
           delimiter=", ", fmt='% s', header='dual_1 vs dummy')
# dummy vs dual_1
np.savetxt("../data/dual/agent_1/battle_data/dummy_vs_dual_1_results.csv", results['dual_1']['vs_dummy']['go_second'],
           delimiter=", ", fmt='% s', header='dummy vs dual')
# dual_2 vs dummy
np.savetxt("../data/dual/agent_2/battle_data/dual_2_vs_dummy_results.csv", results['dual_2']['vs_dummy']['go_first'],
           delimiter=", ", fmt='% s', header='dual_2 vs dummy')
# dummy vs dual_2
np.savetxt("../data/dual/agent_2/battle_data/dummy_vs_dual_2_results.csv", results['dual_2']['vs_dummy']['go_second'],
           delimiter=", ", fmt='% s', header='dummy vs dual_2')

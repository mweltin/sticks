import os
import numpy as np
from agent.player import Player
from agent.battle import Battle
import argparse


def main(num_episodes):
    number_of_training_runs = num_episodes

    results = {
        'dummy':
            {
                'vs_qlearning': [],
                'vs_wolf': [],
                'vs_dqn': [],
                'vs_dual_1': [],
                'vs_dual_2': []
            },
        'qlearning':
            {
                'vs_dummy': [],
                'vs_wolf': [],
                'vs_dqn': [],
                'vs_dual_1': [],
                'vs_dual_2': []
            },
        'wolf':
            {
                'vs_dummy': [],
                'vs_qlearning': [],
                'vs_dqn': [],
                'vs_dual_1': [],
                'vs_dual_2': [],
            },
        'dqn':
            {
                'vs_dummy': [],
                'vs_qlearning': [],
                'vs_wolf': [],
                'vs_dual_1': [],
                'vs_dual_2': [],

            },
        'dual_1':
            {
                'vs_dummy': [],
                'vs_qlearning': [],
                'vs_wolf': [],
                'vs_dqn': [],
                'vs_dual_2': []
            },
        'dual_2':
            {
                'vs_dummy': [],
                'vs_qlearning': [],
                'vs_wolf': [],
                'vs_dqn': [],
                'vs_dual_1': [],
            }
    }

    for i in range(number_of_training_runs):
        # train with the three different algorithms
        os.system("python ../training/qlearning.py --skip_plot=True")
        os.system("python ../training/wolf.py --skip_plot=True")
        os.system("python ../training/dqn.py --skip_plot=True")
        os.system("python ../training/dual_agent.py --skip_plot=True")

        qlearning_q_table = np.genfromtxt('../data/qlearning/q_table.csv', delimiter=',')
        wolf_q_table = np.genfromtxt('../data/wolf/q_table.csv', delimiter=',')
        dqn_q_table = np.genfromtxt('../data/dqn/q_table.csv', delimiter=',')
        dual_1_q_table = np.genfromtxt('../data/dual/agent_1/q_table.csv', delimiter=',')
        dual_2_q_table = np.genfromtxt('../data/dual/agent_2/q_table.csv', delimiter=',')

        q_player = Player(q_table=qlearning_q_table, name='ql_player', strategy='strict')
        wolf_player = Player(q_table=wolf_q_table, name='wolf_player', strategy='strict')
        dqn_player = Player(q_table=dqn_q_table, name='dqn_player', strategy='strict')
        dual_1_player = Player(q_table=dual_1_q_table, name='dual_1_player', strategy='strict')
        dual_2_player = Player(q_table=dual_2_q_table, name='dual_2_player', strategy='strict')
        dummy_player = Player(name='dummy', strategy='random')

        #################### dummy ################################
        # dummy vs qlearning
        battle = Battle(dummy_player, q_player)
        winner = battle.battle()
        results['dummy']['vs_qlearning'].append(winner)

        # dummy vs wolf
        battle = Battle(dummy_player, wolf_player)
        winner = battle.battle()
        results['dummy']['vs_wolf'].append(winner)

        # dummy vs dqn
        battle = Battle(dummy_player, dqn_player)
        winner = battle.battle()
        results['dummy']['vs_dqn'].append(winner)

        # dummy vs dual_1
        battle = Battle(dummy_player, dual_1_player)
        winner = battle.battle()
        results['dummy']['vs_dual_1'].append(winner)

        # dummy vs dual 2
        battle = Battle(dummy_player, dual_2_player)
        winner = battle.battle()
        results['dummy']['vs_dual_2'].append(winner)
        #################### end dummy ################################

        #################### q_learning ################################
        # q_learning vs dummy
        battle = Battle(q_player, dummy_player)
        winner = battle.battle()
        results['qlearning']['vs_dummy'].append(winner)

        # qlearning vs wolf
        battle = Battle(q_player, wolf_player)
        winner = battle.battle()
        results['qlearning']['vs_wolf'].append(winner)

        # qlearning vs dqn
        battle = Battle(q_player, dqn_player)
        winner = battle.battle()
        results['qlearning']['vs_dqn'].append(winner)

        # qlearning vs dual_1
        battle = Battle(q_player, dual_1_player)
        winner = battle.battle()
        results['qlearning']['vs_dual_1'].append(winner)

        # qlearning vs dual_2
        battle = Battle(q_player, dual_2_player)
        winner = battle.battle()
        results['qlearning']['vs_dual_2'].append(winner)

        #################### end q_learning ################################

        #################### wolf ################################

        # wolf vs dummy
        battle = Battle(wolf_player, dummy_player)
        winner = battle.battle()
        results['wolf']['vs_dummy'].append(winner)

        # wolf vs qlearning
        battle = Battle(wolf_player, q_player)
        winner = battle.battle()
        results['wolf']['vs_qlearning'].append(winner)

        # wolf vs dqn
        battle = Battle(q_player, dqn_player)
        winner = battle.battle()
        results['wolf']['vs_dqn'].append(winner)

        # wolf vs dual_1
        battle = Battle(wolf_player, dual_1_player)
        winner = battle.battle()
        results['wolf']['vs_dual_1'].append(winner)

        # wolf vs dual_2
        battle = Battle(wolf_player, dual_2_player)
        winner = battle.battle()
        results['wolf']['vs_dual_2'].append(winner)

        #################### end wolf ################################

        #################### dqn ################################
        # dqn vs dummy
        battle = Battle(dqn_player, dummy_player)
        winner = battle.battle()
        results['dqn']['vs_dummy'].append(winner)

        # dqn vs qlearning
        battle = Battle(dqn_player, q_player)
        winner = battle.battle()
        results['dqn']['vs_qlearning'].append(winner)

        # dqn vs wolf
        battle = Battle(dqn_player, q_player)
        winner = battle.battle()
        results['dqn']['vs_wolf'].append(winner)

        # dqn vs dual_1
        battle = Battle(dqn_player, dual_1_player)
        winner = battle.battle()
        results['dqn']['vs_dual_1'].append(winner)

        # dqn vs dual_2
        battle = Battle(dqn_player, dual_2_player)
        winner = battle.battle()
        results['dqn']['vs_dual_2'].append(winner)
        #################### end dqn ################################

        #################### dual 1 ################################
        # dual 1 vs dummy
        battle = Battle(dual_1_player, dummy_player)
        winner = battle.battle()
        results['dual_1']['vs_dummy'].append(winner)

        # dual_1 vs qlearning
        battle = Battle(dual_1_player, q_player)
        winner = battle.battle()
        results['dual_1']['vs_qlearning'].append(winner)

        # dual 1 vs wolf
        battle = Battle(dual_1_player, wolf_player)
        winner = battle.battle()
        results['dual_1']['vs_wolf'].append(winner)

        # dual 1 vs dqn
        battle = Battle(dual_1_player, dqn_player)
        winner = battle.battle()
        results['dual_1']['vs_dqn'].append(winner)

        # dual 1 vs dual 2
        battle = Battle(dual_1_player, dual_2_player)
        winner = battle.battle()
        results['dual_1']['vs_dual_2'].append(winner)
        #################### end dual 1 ################################

        #################### dual 2 ################################
        # dual 2 vs dummy
        battle = Battle(dual_2_player, dummy_player)
        winner = battle.battle()
        results['dual_2']['vs_dummy'].append(winner)

        # dual_2 vs qlearning
        battle = Battle(dual_2_player, q_player)
        winner = battle.battle()
        results['dual_2']['vs_qlearning'].append(winner)

        # dual 2 vs wolf
        battle = Battle(dual_2_player, wolf_player)
        winner = battle.battle()
        results['dual_2']['vs_wolf'].append(winner)

        # dual 2 vs dqn
        battle = Battle(dual_2_player, dqn_player)
        winner = battle.battle()
        results['dual_2']['vs_dqn'].append(winner)

        # dual 2 vs dual 1
        battle = Battle(dual_2_player, dual_1_player)
        winner = battle.battle()
        results['dual_2']['vs_dual_1'].append(winner)
        #################### end dual 2 ################################

        print(" iteration: " + str(i) + " ")

    # save results  naming convention player 1 vs player 2,  player 1 always went first


    # dummy vs qlearning
    np.savetxt("../data/qlearning/battle_data/dummy_vs_qlearning_results.csv", results['dummy']['vs_qlearning'],
               delimiter=", ", fmt='% s', header='dummy vs ql_player')

    # dummy vs wolf
    np.savetxt("../data/wolf/battle_data/dummy_vs_wolf_results.csv", results['dummy']['vs_wolf'],
               delimiter=", ", fmt='% s', header='dummy vs wolf_player')

    # dummy vs dqn
    np.savetxt("../data/dqn/battle_data/dummy_vs_dqn_results.csv", results['dummy']['vs_dqn'],
               delimiter=", ", fmt='% s', header='dummy vs dqn_player')

    # dummy vs dual_1
    np.savetxt("../data/dual/agent_1/battle_data/dummy_vs_dual_1_results.csv", results['dummy']['vs_dual_1'],
               delimiter=", ", fmt='% s', header='dummy vs dual_1_player')

    # dummy vs dual_2
    np.savetxt("../data/dual/agent_2/battle_data/dummy_vs_dual_2_results.csv", results['dummy']['vs_dual_2'],
               delimiter=", ", fmt='% s', header='dummy vs dual_2_player')




    # qlearning vs dummy
    np.savetxt("../data/qlearning/battle_data/qlearning_vs_dummy_results.csv", results['qlearning']['vs_dummy'],
               delimiter=", ", fmt='% s', header='ql_player vs dummy')

    # qlearning vs wolf_player
    np.savetxt("../data/qlearning/battle_data/ql_vs_wolf_results.csv", results['qlearning']['vs_wolf'],
               delimiter=", ", fmt='% s', header='ql_player vs wolf_player')

    # qlearning vs dqn_player
    np.savetxt("../data/qlearning/battle_data/ql_vs_dqn_results.csv", results['qlearning']['vs_dqn'],
               delimiter=", ", fmt='% s', header='ql_player vs dqn_player')

    # qlearning vs dual_1
    np.savetxt("../data/qlearning/battle_data/ql_vs_dual_1_results.csv", results['qlearning']['vs_dual_1'],
               delimiter=", ", fmt='% s', header='ql_player vs dual_1_player')

    # qlearning vs dual_2
    np.savetxt("../data/qlearning/battle_data/ql_vs_dual_2_results.csv", results['qlearning']['vs_dual_2'],
               delimiter=", ", fmt='% s', header='ql_player vs dual_2_player')




    # wolf vs dummy
    np.savetxt("../data/wolf/battle_data/wolf_vs_dummy_results.csv", results['wolf']['vs_dummy'],
               delimiter=", ", fmt='% s', header='wolf_player vs dummy')

    # wolf vs qlearning
    np.savetxt("../data/qlearning/battle_data/wolf_vs_ql_results.csv", results['wolf']['vs_qlearning'],
               delimiter=", ", fmt='% s', header='wolf_player vs ql_player')

    # wolf vs dqn
    np.savetxt("../data/wolf/battle_data/wolf_vs_dqn_results.csv", results['wolf']['vs_dqn'],
               delimiter=", ", fmt='% s', header='wolf_player vs dqn')

    # wolf vs dual_1
    np.savetxt("../data/wolf/battle_data/wolf_vs_dual_1_results.csv", results['wolf']['vs_dual_1'],
               delimiter=", ", fmt='% s', header='wolf_player vs dual_1_player')

    # wolf vs dual_2
    np.savetxt("../data/wolf/battle_data/wolf_vs_dual_2_results.csv", results['wolf']['vs_dual_2'],
               delimiter=", ", fmt='% s', header='wolf_player vs dual_2_player')



    # dqn vs dummy
    np.savetxt("../data/dqn/battle_data/dqn_vs_dummy_results.csv", results['dqn']['vs_dummy'],
               delimiter=", ", fmt='% s', header='dqn_player vs dummy')

    # dqn vs qlearning
    np.savetxt("../data/qlearning/battle_data/dqn_vs_ql_results.csv", results['dqn']['vs_qlearning'],
               delimiter=", ", fmt='% s', header='dqn_player vs ql_player')

    # dqn vs wolf
    np.savetxt("../data/qlearning/battle_data/dqn_vs_wolf_results.csv", results['dqn']['vs_wolf'],
               delimiter=", ", fmt='% s', header='dqn_player vs wolf_player')

    # dqn vs dual_1
    np.savetxt("../data/dqn/battle_data/dqn_vs_dual_1_results.csv", results['dqn']['vs_dual_1'],
               delimiter=", ", fmt='% s', header='dqn_player vs dual_1_player')

    # dqn vs dual_2
    np.savetxt("../data/dqn/battle_data/dqn_vs_dual_2_results.csv", results['dqn']['vs_dual_2'],
               delimiter=", ", fmt='% s', header='dqn_player vs dual_2_player')



    # dual_1 vs dummy
    np.savetxt("../data/dual/agent_1/battle_data/dual_1_vs_dummy_results.csv", results['dual_1']['vs_dummy'],
               delimiter=", ", fmt='% s', header='dual_1_player vs dummy')

    # dual_1 vs qlearning
    np.savetxt("../data/qlearning/battle_data/dual_1_vs_ql_results.csv", results['dual_1']['vs_qlearning'],
               delimiter=", ", fmt='% s', header='dual_1_player vs ql_player')

    # dual_1 vs wolf
    np.savetxt("../data/wolf/battle_data/dual_1_vs_wolf_results.csv", results['dual_1']['vs_wolf'],
               delimiter=", ", fmt='% s', header='dual_1_player vs wolf_player')

    # dual_1 vs dqn
    np.savetxt("../data/dqn/battle_data/dual_1_vs_dqn_results.csv", results['dual_1']['vs_dqn'],
               delimiter=", ", fmt='% s', header='dual_1_player vs dqn_player')

    # dual 1 vs dual 2
    np.savetxt("../data/dual/agent_1/battle_data/dual_1_vs_dual_2.csv", results['dual_1']['vs_dual_2'],
               delimiter=", ", fmt='% s', header='dual_1_player vs dual_2_player')


    # dual_2 vs dummy
    np.savetxt("../data/dual/agent_2/battle_data/dual_2_vs_dummy_results.csv", results['dual_2']['vs_dummy'],
               delimiter=", ", fmt='% s', header='dual_2_player vs dummy')

    # dual_2 vs qlearning
    np.savetxt("../data/qlearning/battle_data/dual_2_vs_ql_results.csv", results['dual_2']['vs_qlearning'],
               delimiter=", ", fmt='% s', header='dual_2_player vs ql_player')

    # dual_2 vs wolf
    np.savetxt("../data/wolf/battle_data/dual_2_vs_wolf_results.csv", results['dual_2']['vs_wolf'],
               delimiter=", ", fmt='% s', header='dual_2_player vs wolf_player')

    # dual_2 vs dqn
    np.savetxt("../data/dqn/battle_data/dual_2_vs_dqn_results.csv", results['dual_2']['vs_dqn'],
               delimiter=", ", fmt='% s', header='dual_2_player vs dqn_player')

    # dual_2 vs dual 1
    np.savetxt("../data/dual/agent_2/battle_data/dual_2_vs_dual_1_results.csv", results['dual_2']['vs_dual_1'],
               delimiter=", ", fmt='% s', header='dual_2_player vs dual_1_player')

    print("train battle done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q-algorithm arguments')
    parser.add_argument('--num_episodes', type=int, default=30,
                        help='how many games to play')
    args = parser.parse_args()
    main(num_episodes=args.num_episodes)

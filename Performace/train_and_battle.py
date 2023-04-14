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

        qlearning = Player(q_table=qlearning_q_table, name='qlearning', strategy='strict')
        wolf = Player(q_table=wolf_q_table, name='wolf', strategy='strict')
        dqn = Player(q_table=dqn_q_table, name='dqn', strategy='strict')
        dual_1 = Player(q_table=dual_1_q_table, name='dual_1', strategy='strict')
        dual_2 = Player(q_table=dual_2_q_table, name='dual_2', strategy='strict')
        dummy = Player(name='dummy', strategy='random')

        #################### dummy ################################
        # dummy vs qlearning
        battle = Battle(dummy, qlearning)
        winner = battle.battle()
        results['dummy']['vs_qlearning'].append(winner)

        # dummy vs wolf
        battle = Battle(dummy, wolf)
        winner = battle.battle()
        results['dummy']['vs_wolf'].append(winner)

        # dummy vs dqn
        battle = Battle(dummy, dqn)
        winner = battle.battle()
        results['dummy']['vs_dqn'].append(winner)

        # dummy vs dual_1
        battle = Battle(dummy, dual_1)
        winner = battle.battle()
        results['dummy']['vs_dual_1'].append(winner)

        # dummy vs dual 2
        battle = Battle(dummy, dual_2)
        winner = battle.battle()
        results['dummy']['vs_dual_2'].append(winner)
        #################### end dummy ################################

        #################### q_learning ################################
        # q_learning vs dummy
        battle = Battle(qlearning, dummy)
        winner = battle.battle()
        results['qlearning']['vs_dummy'].append(winner)

        # qlearning vs wolf
        battle = Battle(qlearning, wolf)
        winner = battle.battle()
        results['qlearning']['vs_wolf'].append(winner)

        # qlearning vs dqn
        battle = Battle(qlearning, dqn)
        winner = battle.battle()
        results['qlearning']['vs_dqn'].append(winner)

        # qlearning vs dual_1
        battle = Battle(qlearning, dual_1)
        winner = battle.battle()
        results['qlearning']['vs_dual_1'].append(winner)

        # qlearning vs dual_2
        battle = Battle(qlearning, dual_2)
        winner = battle.battle()
        results['qlearning']['vs_dual_2'].append(winner)

        #################### end q_learning ################################

        #################### wolf ################################

        # wolf vs dummy
        battle = Battle(wolf, dummy)
        winner = battle.battle()
        results['wolf']['vs_dummy'].append(winner)

        # wolf vs qlearning
        battle = Battle(wolf, qlearning)
        winner = battle.battle()
        results['wolf']['vs_qlearning'].append(winner)

        # wolf vs dqn
        battle = Battle(qlearning, dqn)
        winner = battle.battle()
        results['wolf']['vs_dqn'].append(winner)

        # wolf vs dual_1
        battle = Battle(wolf, dual_1)
        winner = battle.battle()
        results['wolf']['vs_dual_1'].append(winner)

        # wolf vs dual_2
        battle = Battle(wolf, dual_2)
        winner = battle.battle()
        results['wolf']['vs_dual_2'].append(winner)

        #################### end wolf ################################

        #################### dqn ################################
        # dqn vs dummy
        battle = Battle(dqn, dummy)
        winner = battle.battle()
        results['dqn']['vs_dummy'].append(winner)

        # dqn vs qlearning
        battle = Battle(dqn, qlearning)
        winner = battle.battle()
        results['dqn']['vs_qlearning'].append(winner)

        # dqn vs wolf
        battle = Battle(dqn, wolf)
        winner = battle.battle()
        results['dqn']['vs_wolf'].append(winner)

        # dqn vs dual_1
        battle = Battle(dqn, dual_1)
        winner = battle.battle()
        results['dqn']['vs_dual_1'].append(winner)

        # dqn vs dual_2
        battle = Battle(dqn, dual_2)
        winner = battle.battle()
        results['dqn']['vs_dual_2'].append(winner)
        #################### end dqn ################################

        #################### dual 1 ################################
        # dual 1 vs dummy
        battle = Battle(dual_1, dummy)
        winner = battle.battle()
        results['dual_1']['vs_dummy'].append(winner)

        # dual_1 vs qlearning
        battle = Battle(dual_1, qlearning)
        winner = battle.battle()
        results['dual_1']['vs_qlearning'].append(winner)

        # dual 1 vs wolf
        battle = Battle(dual_1, wolf)
        winner = battle.battle()
        results['dual_1']['vs_wolf'].append(winner)

        # dual 1 vs dqn
        battle = Battle(dual_1, dqn)
        winner = battle.battle()
        results['dual_1']['vs_dqn'].append(winner)

        # dual 1 vs dual 2
        battle = Battle(dual_1, dual_2)
        winner = battle.battle()
        results['dual_1']['vs_dual_2'].append(winner)
        #################### end dual 1 ################################

        #################### dual 2 ################################
        # dual 2 vs dummy
        battle = Battle(dual_2, dummy)
        winner = battle.battle()
        results['dual_2']['vs_dummy'].append(winner)

        # dual_2 vs qlearning
        battle = Battle(dual_2, qlearning)
        winner = battle.battle()
        results['dual_2']['vs_qlearning'].append(winner)

        # dual 2 vs wolf
        battle = Battle(dual_2, wolf)
        winner = battle.battle()
        results['dual_2']['vs_wolf'].append(winner)

        # dual 2 vs dqn
        battle = Battle(dual_2, dqn)
        winner = battle.battle()
        results['dual_2']['vs_dqn'].append(winner)

        # dual 2 vs dual 1
        battle = Battle(dual_2, dual_1)
        winner = battle.battle()
        results['dual_2']['vs_dual_1'].append(winner)
        #################### end dual 2 ################################

        print(" iteration: " + str(i) + " ")

    # save results  naming convention player 1 vs player 2,  player 1 always went first


    # dummy vs qlearning
    np.savetxt("../data/dummy/battle_data/dummy_vs_qlearning_results.csv", results['dummy']['vs_qlearning'],
               delimiter=", ", fmt='% s', header='dummy vs qlearning')

    # dummy vs wolf
    np.savetxt("../data/dummy//battle_data/dummy_vs_wolf_results.csv", results['dummy']['vs_wolf'],
               delimiter=", ", fmt='% s', header='dummy vs wolf')

    # dummy vs dqn
    np.savetxt("../data/dummy//battle_data/dummy_vs_dqn_results.csv", results['dummy']['vs_dqn'],
               delimiter=", ", fmt='% s', header='dummy vs dqn')

    # dummy vs dual_1
    np.savetxt("../data/dummy/battle_data/dummy_vs_dual_1_results.csv", results['dummy']['vs_dual_1'],
               delimiter=", ", fmt='% s', header='dummy vs dual_1')

    # dummy vs dual_2
    np.savetxt("../data/dummy/battle_data/dummy_vs_dual_2_results.csv", results['dummy']['vs_dual_2'],
               delimiter=", ", fmt='% s', header='dummy vs dual_2')




    # qlearning vs dummy
    np.savetxt("../data/qlearning/battle_data/qlearning_vs_dummy_results.csv", results['qlearning']['vs_dummy'],
               delimiter=", ", fmt='% s', header='qlearning vs dummy')

    # qlearning vs wolf
    np.savetxt("../data/qlearning/battle_data/qlearning_vs_wolf_results.csv", results['qlearning']['vs_wolf'],
               delimiter=", ", fmt='% s', header='qlearning vs wolf')

    # qlearning vs dqn
    np.savetxt("../data/qlearning/battle_data/qlearning_vs_dqn_results.csv", results['qlearning']['vs_dqn'],
               delimiter=", ", fmt='% s', header='qlearning vs dqn')

    # qlearning vs dual_1
    np.savetxt("../data/qlearning/battle_data/qlearning_vs_dual_1_results.csv", results['qlearning']['vs_dual_1'],
               delimiter=", ", fmt='% s', header='qlearning vs dual_1')

    # qlearning vs dual_2
    np.savetxt("../data/qlearning/battle_data/qlearning_vs_dual_2_results.csv", results['qlearning']['vs_dual_2'],
               delimiter=", ", fmt='% s', header='qlearning vs dual_2')




    # wolf vs dummy
    np.savetxt("../data/wolf/battle_data/wolf_vs_dummy_results.csv", results['wolf']['vs_dummy'],
               delimiter=", ", fmt='% s', header='wolf vs dummy')

    # wolf vs qlearning
    np.savetxt("../data/wolf/battle_data/wolf_vs_ql_results.csv", results['wolf']['vs_qlearning'],
               delimiter=", ", fmt='% s', header='wolf vs qlearning')

    # wolf vs dqn
    np.savetxt("../data/wolf/battle_data/wolf_vs_dqn_results.csv", results['wolf']['vs_dqn'],
               delimiter=", ", fmt='% s', header='wolf vs dqn')

    # wolf vs dual_1
    np.savetxt("../data/wolf/battle_data/wolf_vs_dual_1_results.csv", results['wolf']['vs_dual_1'],
               delimiter=", ", fmt='% s', header='wolf vs dual_1')

    # wolf vs dual_2
    np.savetxt("../data/wolf/battle_data/wolf_vs_dual_2_results.csv", results['wolf']['vs_dual_2'],
               delimiter=", ", fmt='% s', header='wolf vs dual_2')



    # dqn vs dummy
    np.savetxt("../data/dqn/battle_data/dqn_vs_dummy_results.csv", results['dqn']['vs_dummy'],
               delimiter=", ", fmt='% s', header='dqn vs dummy')

    # dqn vs qlearning
    np.savetxt("../data/dqn/battle_data/dqn_vs_ql_results.csv", results['dqn']['vs_qlearning'],
               delimiter=", ", fmt='% s', header='dqn vs qlearning')

    # dqn vs wolf
    np.savetxt("../data/dqn/battle_data/dqn_vs_wolf_results.csv", results['dqn']['vs_wolf'],
               delimiter=", ", fmt='% s', header='dqn vs wolf')

    # dqn vs dual_1
    np.savetxt("../data/dqn/battle_data/dqn_vs_dual_1_results.csv", results['dqn']['vs_dual_1'],
               delimiter=", ", fmt='% s', header='dqn vs dual_1')

    # dqn vs dual_2
    np.savetxt("../data/dqn/battle_data/dqn_vs_dual_2_results.csv", results['dqn']['vs_dual_2'],
               delimiter=", ", fmt='% s', header='dqn vs dual_2')



    # dual_1 vs dummy
    np.savetxt("../data/dual/agent_1/battle_data/dual_1_vs_dummy_results.csv", results['dual_1']['vs_dummy'],
               delimiter=", ", fmt='% s', header='dual_1 vs dummy')

    # dual_1 vs qlearning
    np.savetxt("../data/dual/agent_1/battle_data/dual_1_vs_ql_results.csv", results['dual_1']['vs_qlearning'],
               delimiter=", ", fmt='% s', header='dual_1 vs ql_player')

    # dual_1 vs wolf
    np.savetxt("../data/dual/agent_1/battle_data/dual_1_vs_wolf_results.csv", results['dual_1']['vs_wolf'],
               delimiter=", ", fmt='% s', header='dual_1 vs wolf')

    # dual_1 vs dqn
    np.savetxt("../data/dual/agent_1/battle_data/dual_1_vs_dqn_results.csv", results['dual_1']['vs_dqn'],
               delimiter=", ", fmt='% s', header='dual_1 vs dqn')

    # dual 1 vs dual 2
    np.savetxt("../data/dual/agent_1/battle_data/dual_1_vs_dual_2.csv", results['dual_1']['vs_dual_2'],
               delimiter=", ", fmt='% s', header='dual_1 vs dual_2')


    # dual_2 vs dummy
    np.savetxt("../data/dual/agent_2/battle_data/dual_2_vs_dummy_results.csv", results['dual_2']['vs_dummy'],
               delimiter=", ", fmt='% s', header='dual_2 vs dummy')

    # dual_2 vs qlearning
    np.savetxt("../data/dual/agent_2/battle_data/dual_2_vs_ql_results.csv", results['dual_2']['vs_qlearning'],
               delimiter=", ", fmt='% s', header='dual_2 vs qlearning')

    # dual_2 vs wolf
    np.savetxt("../data/dual/agent_2/battle_data/dual_2_vs_wolf_results.csv", results['dual_2']['vs_wolf'],
               delimiter=", ", fmt='% s', header='dual_2 vs wolf')

    # dual_2 vs dqn
    np.savetxt("../data/dual/agent_2/battle_data/dual_2_vs_dqn_results.csv", results['dual_2']['vs_dqn'],
               delimiter=", ", fmt='% s', header='dual_2 vs dqn')

    # dual_2 vs dual 1
    np.savetxt("../data/dual/agent_2/battle_data/dual_2_vs_dual_1_results.csv", results['dual_2']['vs_dual_1'],
               delimiter=", ", fmt='% s', header='dual_2 vs dual_1')

    print("train battle done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q-algorithm arguments')
    parser.add_argument('--num_episodes', type=int, default=30,
                        help='how many games to play')
    args = parser.parse_args()
    main(num_episodes=args.num_episodes)

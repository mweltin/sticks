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
                'vs_dqn': [],
            },
        'dqn':
            {
                'vs_dummy': [],
            }
    }

    for i in range(number_of_training_runs):
        # train with the three different algorithms

        os.system("python ../training/dqn.py --skip_plot=True")

        dqn_q_table = np.genfromtxt('../data/dqn/q_table.csv', delimiter=',')

        dqn = Player(q_table=dqn_q_table, name='dqn', strategy='strict')

        dummy = Player(name='dummy', strategy='random')

        #################### dqn ################################
        # dqn vs dummy
        battle = Battle(dqn, dummy)
        winner = battle.battle()
        results['dqn']['vs_dummy'].append(winner)

        battle = Battle(dummy, dqn)
        winner = battle.battle()
        results['dummy']['vs_dqn'].append(winner)

        #################### end dqn ################################

        print(" iteration: " + str(i) + " ")

    # save results  naming convention player 1 vs player 2,  player 1 always went first

    # dummy vs dqn
    np.savetxt("../data/dummy/battle_data/dummy_vs_dqn_results.csv", results['dummy']['vs_dqn'],
               delimiter=", ", fmt='% s', header='dummy vs dqn')

    # dqn vs dummy
    np.savetxt("../data/dqn/battle_data/dqn_vs_dummy_results.csv", results['dqn']['vs_dummy'],
               delimiter=", ", fmt='% s', header='dqn vs dummy')

    print("train battle done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q-algorithm arguments')
    parser.add_argument('--num_episodes', type=int, default=30,
                        help='how many games to play')
    args = parser.parse_args()
    main(num_episodes=args.num_episodes)

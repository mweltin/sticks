import csv
import numpy as np


def main():
    # save results  naming convention player 1 vs player 2,  player 1 always went first
    # qlearning vs dummy
    datafiles = ["../data/qlearning/battle_data/gl_vs_dummy_results.csv",
                 "../data/qlearning/battle_data/dummy_vs_ql_results.csv",
                 "../data/qlearning/battle_data/ql_vs_wolf_results.csv",
                 "../data/qlearning/battle_data/wolf_vs_ql_results.csv",
                 "../data/qlearning/battle_data/ql_vs_dual_1_results.csv",
                 "../data/qlearning/battle_data/dual_1_vs_ql_results.csv",
                 "../data/qlearning/battle_data/ql_vs_dual_2_results.csv",
                 "../data/qlearning/battle_data/dual_2_vs_ql_results.csv",
                 "../data/wolf/battle_data/wolf_vs_dummy_results.csv",
                 "../data/wolf/battle_data/dummy_vs_wolf_results.csv",
                 "../data/wolf/battle_data/wolf_vs_dual_1_results.csv",
                 "../data/wolf/battle_data/dual_1_vs_wolf_results.csv",
                 "../data/wolf/battle_data/wolf_vs_dual_2_results.csv",
                 "../data/wolf/battle_data/dual_2_vs_wolf_results.csv",
                 "../data/dual/agent_1/battle_data/dual_1_vs_dummy_results.csv",
                 "../data/dual/agent_1/battle_data/dummy_vs_dual_1_results.csv",
                 "../data/dual/agent_2/battle_data/dual_2_vs_dummy_results.csv",
                 "../data/dual/agent_2/battle_data/dummy_vs_dual_2_results.csv",
                 ]
    results = [['player 1', 'player 2', 'wins', 'losses', 'draws', 'performance']]

    for dfile in datafiles:
        with open(dfile, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        players = data[0][0].split()
        temp = {players[1]: 0, players[3]: 0, 'Draw': 0}

        for e in data[1:]:
            if e[0] not in temp.keys():
                raise
            temp[e[0]] += 1

        total_games = temp[players[1]] + temp[players[3]] + temp['Draw']
        total_wins = temp[players[1]] + temp['Draw']
        performance = round(total_wins / total_games, 4)
        line_item = [players[1], players[3], temp[players[1]], temp[players[3]], temp['Draw'], performance]

        results.append(line_item)

    np.savetxt("final_results.csv",
               results,
               delimiter=", ",
               fmt='% s')


if __name__ == '__main__':
    main()

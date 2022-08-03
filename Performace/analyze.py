import csv
import numpy as np


def main():
    # save results  naming convention player 1 vs player 2,  player 1 always went first
    # qlearning vs dummy
    root_dir = '/Users/mweltin/data_report_results'
    datafiles = [root_dir + "/qlearning/battle_data/gl_vs_dummy_results.csv",
                 root_dir + "/qlearning/battle_data/dummy_vs_ql_results.csv",
                 root_dir + "/qlearning/battle_data/ql_vs_wolf_results.csv",
                 root_dir + "/qlearning/battle_data/wolf_vs_ql_results.csv",
                 root_dir + "/qlearning/battle_data/ql_vs_dual_1_results.csv",
                 root_dir + "/qlearning/battle_data/dual_1_vs_ql_results.csv",
                 root_dir + "/qlearning/battle_data/ql_vs_dual_2_results.csv",
                 root_dir + "/qlearning/battle_data/dual_2_vs_ql_results.csv",
                 root_dir + "/wolf/battle_data/wolf_vs_dummy_results.csv",
                 root_dir + "/wolf/battle_data/dummy_vs_wolf_results.csv",
                 root_dir + "/wolf/battle_data/wolf_vs_dual_1_results.csv",
                 root_dir + "/wolf/battle_data/dual_1_vs_wolf_results.csv",
                 root_dir + "/wolf/battle_data/wolf_vs_dual_2_results.csv",
                 root_dir + "/wolf/battle_data/dual_2_vs_wolf_results.csv",
                 root_dir + "/dual/agent_1/battle_data/dual_1_vs_dummy_results.csv",
                 root_dir + "/dual/agent_1/battle_data/dummy_vs_dual_1_results.csv",
                 root_dir + "/dual/agent_2/battle_data/dual_2_vs_dummy_results.csv",
                 root_dir + "/dual/agent_2/battle_data/dummy_vs_dual_2_results.csv",
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

    exit()


if __name__ == '__main__':
    main()

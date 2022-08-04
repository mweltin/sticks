import csv
import numpy as np

"/qlearning/battle_data/qlearning_vs_dummy_results.csv",
"/qlearning/battle_data/dummy_vs_qlearning_results.csv",
"/wolf/battle_data/wolf_vs_dummy_results.csv",
"/wolf/battle_data/dummy_vs_wolf_results.csv",
"/dual/agent_1/battle_data/dual_1_vs_dummy_results.csv",
"/dual/agent_1/battle_data/dummy_vs_dual_1_results.csv",
"/dual/agent_2/battle_data/dual_2_vs_dummy_results.csv",
"/dual/agent_2/battle_data/dummy_vs_dual_2_results.csv",
"/qlearning/battle_data/ql_vs_wolf_results.csv",
"/qlearning/battle_data/wolf_vs_ql_results.csv",
"/qlearning/battle_data/ql_vs_dual_1_results.csv",
"/qlearning/battle_data/dual_1_vs_ql_results.csv",
"/qlearning/battle_data/ql_vs_dual_2_results.csv",
"/qlearning/battle_data/dual_2_vs_ql_results.csv",
"/wolf/battle_data/wolf_vs_dual_1_results.csv",
"/wolf/battle_data/dual_1_vs_wolf_results.csv",
"/wolf/battle_data/wolf_vs_dual_2_results.csv",
"/wolf/battle_data/dual_2_vs_wolf_results.csv",
"/dual/dual_1/battle_data/dual_1_vs_dual_2.csv",
"/dual/dual_2/battle_data/dual_2_vs_dual_1_results.csv",


def main():
    # save results  naming convention player 1 vs player 2,  player 1 always went first
    # qlearning vs dummy
    root_dir = '/Users/mweltin/AI-801/project/sticks/data'
    datafiles = [
        root_dir + "/qlearning/battle_data/qlearning_vs_dummy_results.csv",
        root_dir + "/qlearning/battle_data/dummy_vs_qlearning_results.csv",
        root_dir + "/wolf/battle_data/wolf_vs_dummy_results.csv",
        root_dir + "/wolf/battle_data/dummy_vs_wolf_results.csv",
        root_dir + "/dual/agent_1/battle_data/dual_1_vs_dummy_results.csv",
        root_dir + "/dual/agent_1/battle_data/dummy_vs_dual_1_results.csv",
        root_dir + "/dual/agent_2/battle_data/dual_2_vs_dummy_results.csv",
        root_dir + "/dual/agent_2/battle_data/dummy_vs_dual_2_results.csv",
        root_dir + "/qlearning/battle_data/ql_vs_wolf_results.csv",
        root_dir + "/qlearning/battle_data/wolf_vs_ql_results.csv",
        root_dir + "/qlearning/battle_data/ql_vs_dual_1_results.csv",
        root_dir + "/qlearning/battle_data/dual_1_vs_ql_results.csv",
        root_dir + "/qlearning/battle_data/ql_vs_dual_2_results.csv",
        root_dir + "/qlearning/battle_data/dual_2_vs_ql_results.csv",
        root_dir + "/wolf/battle_data/wolf_vs_dual_1_results.csv",
        root_dir + "/wolf/battle_data/dual_1_vs_wolf_results.csv",
        root_dir + "/wolf/battle_data/wolf_vs_dual_2_results.csv",
        root_dir + "/wolf/battle_data/dual_2_vs_wolf_results.csv",
        root_dir + "/dual/agent_1/battle_data/dual_1_vs_dual_2.csv",
        root_dir + "/dual/agent_2/battle_data/dual_2_vs_dual_1_results.csv",
    ]
    results = [['player 1', 'player 2', 'wins', 'losses', 'draws', 'performance player 1', 'performance player 2']]

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

        total_wins_p1 = temp[players[1]] + temp['Draw']
        performance_p1 = round(total_wins_p1 / total_games, 4)

        total_wins_p2 = temp[players[3]] + temp['Draw']
        performance_p2 = round(total_wins_p2 / total_games, 4)

        line_item = [players[1], players[3], temp[players[1]], temp[players[3]], temp['Draw'], performance_p1, performance_p2]

        results.append(line_item)

    np.savetxt("./final_results.csv",
               results,
               delimiter=", ",
               fmt='% s')

    print("done analyze")
    exit()


if __name__ == '__main__':
    main()

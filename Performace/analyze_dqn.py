import csv
import numpy as np
from pathlib import Path


def main():
    # save results  naming convention player 1 vs player 2,  player 1 always went first
    # qlearning vs dummy
    root_dir = Path('../data/')
    datafiles = [
        root_dir / 'dummy' / 'battle_data' / 'dummy_vs_dqn_results.csv',
        root_dir / 'dqn' / 'battle_data' / 'dqn_vs_dummy_results.csv',
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

        line_item = [players[1], players[3], temp[players[1]], temp[players[3]], temp['Draw'], performance_p1,
                     performance_p2]

        results.append(line_item)

    np.savetxt("./final_results.csv",
               results,
               delimiter=", ",
               fmt='% s')

    print("done analyze")
    exit()


if __name__ == '__main__':
    main()

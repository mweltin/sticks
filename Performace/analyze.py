import csv


def main(file):
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

    with open(file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    temp = {}

    for e in data[1:]:
        if e[0] not in temp.keys():
            temp[e[0]] = 0
        temp[e[0]] += 1

    pass


if __name__ == '__main__':
    main()

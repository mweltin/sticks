import environment.env as env
from os.path import exists
import matplotlib.pyplot as plt
import numpy as np
import random
import rules.rules as rules


class Utility:

    def __init__(self, base_directory=None):
        if not base_directory:
            raise
        self.base_directory = base_directory

    def save_output(self, input_table, prefix=None):
        file_name = "q_table"
        if prefix:
            file_name = file_name + "_" + str(prefix)

        retval = []
        for idx, value in enumerate(input_table):
            temp = [*env.state_table[idx][0], *env.state_table[idx][1], *value]
            retval.append(temp)

        np.savetxt(self.base_directory+"/state_" + file_name + ".csv",
                   retval,
                   delimiter=", ",
                   fmt='% s',
                   header='AI L, AI R, O L, O R, swap, L L, L R, R R, R L')

        np.savetxt(self.base_directory+"/" + file_name + ".csv",
                   input_table,
                   delimiter=", ",
                   fmt='% s')

    def load_max_reward_q_table(self):
        file_exists = exists(self.base_directory+"/q_table_max_reward.csv")
        if file_exists:
            data = np.genfromtxt(self.base_directory+"/q_table_max_reward.csv", delimiter=',')
            return data
        else:
            return False

    def plot_it(self, data, num):
        """
        actually plots the reward_vs_episode graph
        :param data:
        :param num:
        :return:
        """
        # x axis values
        x = range(1, len(data) + 1)
        # corresponding y axis values
        y = data

        # plotting the points
        plt.plot(x, y)

        # naming the x axis
        plt.xlabel('Epoch')
        # naming the y axis
        plt.ylabel('Reward')

        # giving a title to my graph
        plt.title('Average reward per ' + str(num) + ' episodes')

        # function to show the plot
        plt.savefig(self.base_directory+'/reward_vs_episode.png')
        plt.show()

    def calc_performance(self, performance_data):
        wins = 0

        for p in performance_data:
            if p[4] == 'Draw' or p[4] == 'AI':
                wins += 1

        return wins / len(performance_data)

    def performance_output(self, performance_data):
        np.savetxt(self.base_directory+"/raw_performance.csv",
                   performance_data,
                   delimiter=", ",
                   fmt='% s',
                   header='episode, exploration_rate, rewards_current_episode, step, winner')

    def agents_turn(self, exploration_rate, q_table, state_idx, _learning_rate, _discount_rate,
                    rewards_current_episode):
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            action = env.nanargmax_unbiased(q_table[state_idx])
        else:
            action = env.select_random_action(state_idx, env.Players.agent)

        new_state_idx, reward, done, info = env.step(state_idx, env.Players.agent, action)
        # Update Q-table for Q(s,a)

        if not done:
            q_table[state_idx][action] = q_table[state_idx][action] * (1 - _learning_rate) + _learning_rate * (
                    reward + _discount_rate * env.nanargmax_unbiased(q_table[new_state_idx]))
        else:
            """if we are done at this point the AI has won.  Winning states have no valid moves. Therefore
            the expression np.nanargmax(q_table[new_state_idx] results in a ValueError and the q_table does
            not get updated.  For the state (0,1)(0,4) it doesn't matter as there is only one move.  However
            (0,4),(0,1) there are two moves: split or right right.  Without this block, only the split move
            would get updated in the q_table"""
            q_table[state_idx][action] = q_table[state_idx][action] * (1 - _learning_rate) + \
                                         _learning_rate * (reward + _discount_rate)

        rules.update_redundant_states(env.state_table[state_idx], q_table[state_idx][action], action, q_table)
        state_idx = new_state_idx
        rewards_current_episode += reward

        return q_table, done, state_idx, rewards_current_episode

    def dummy_turn(self, opponent_q_table, _use_q_table_for_actions, state_idx):
        # opponents turn
        if type(opponent_q_table) == np.ndarray and _use_q_table_for_actions is True:
            action = env.nanargmax_unbiased(opponent_q_table[state_idx])
        else:
            action = env.select_random_action(state_idx, 1)
        new_state_idx, reward, done, info = env.step(state_idx, env.Players.opponent, action)
        state_idx = new_state_idx

        return state_idx, done

"""
Implementation of a Q-Learning algorithm to learn to game of sticks
Author: Markus Weltin
"""
import numpy as np
import random
import environment.env as env
import argparse
from os.path import exists
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Process some integers.')


def main(
        num_episodes,
        max_steps_per_episode,
        learning_rate,
        discount_rate,
        min_exploration_rate,
        exploration_decay_rate,
        use_q_table_for_actions
):
    action_space_size = len(env.action_table)
    state_space_size = len(env.state_table)

    ''' initialize q-table with all zeros, i.e. no knowledge'''
    q_table = np.zeros((state_space_size, action_space_size))
    env.eliminate_invalid_actions(env.state_table, q_table)
    opponent_q_table = load_max_reward_q_table()

    '''how many games to play'''
    _num_episodes = num_episodes
    ''' how many turns to take in a game before starting a new game. '''
    _max_steps_per_episode = max_steps_per_episode

    _use_q_table_for_actions = use_q_table_for_actions

    '''learning rate how quickly the agent abandons the previous q value in the 
        qtable for a new q value for a give (state, action) pair.  
        The higher the learning rate the quicker the agent will adopt the new
        q value. '''
    _learning_rate = learning_rate
    _discount_rate = discount_rate

    '''The following values control the exploration / exploitation of the agent'''
    exploration_rate = 1
    max_exploration_rate = 1
    _min_exploration_rate = min_exploration_rate
    _exploration_decay_rate = exploration_decay_rate

    rewards_all_episodes = []
    '''used to decide when to save a q table always save last table and highest reward table'''

    '''flag used to trigger the saving of the current q_table that has the highest reward'''
    max_reward = 0
    '''Agent performance dictionary used to collect episode out put performance = (wins+draws)/(total episodes)'''
    '''Elements include "episode", "exploration rate", "reward", "turn", "winner"'''
    performance = []

    # Q-learning algorithm
    for episode in range(_num_episodes):
        finished_on = 'Draw'
        # initialize new episode params
        state_idx = env.reset()  # state is the index in the env.state_table
        rewards_current_episode = 0

        for step in range(_max_steps_per_episode):
            # Exploration-exploitation trade-off
            # Take new action
            # Update Q-table
            # Set new state
            # Add new reward
            exploration_rate_threshold = random.uniform(0, 1)
            if exploration_rate_threshold > exploration_rate:
                action = np.nanargmax(q_table[state_idx])
            else:
                action = env.select_random_action(state_idx, env.Players.agent)

            new_state_idx, reward, done, info = env.step(state_idx, env.Players.agent, action)
            # Update Q-table for Q(s,a)

            if not done:
                q_table[state_idx][action] = q_table[state_idx][action] * (1 - _learning_rate) + \
                    _learning_rate * (reward + _discount_rate * np.nanargmax(q_table[new_state_idx]))
            else:
                """if we are done at this point the AI has won.  Winning states have no valid moves. Therefore
                the expression np.nanargmax(q_table[new_state_idx] results in a ValueError and the q_table does
                not get updated.  For the state (0,1)(0,4) it doesn't matter as there is only one move.  However
                (0,4),(0,1) there are two moves: split or right right.  Without this block, only the split move
                would get updated in the q_table"""
                q_table[state_idx][action] = q_table[state_idx][action] * (1 - _learning_rate) + \
                    _learning_rate * (reward + _discount_rate)

            state_idx = new_state_idx
            rewards_current_episode += reward

            if done:
                finished_on = 'AI'
                break

            # opponents turn
            if type(opponent_q_table) == np.ndarray and _use_q_table_for_actions is True:
                action = np.nanargmax(opponent_q_table[state_idx])
            else:
                action = env.select_random_action(state_idx, 1)
            new_state_idx, reward, done, info = env.step(state_idx, env.Players.opponent, action)
            state_idx = new_state_idx

            if done:
                finished_on = 'Opponent'
                break
        # Exploration rate decay
        exploration_rate = _min_exploration_rate + \
                           (max_exploration_rate - _min_exploration_rate) * np.exp(-_exploration_decay_rate * episode)

        performance.append([episode, exploration_rate, rewards_current_episode, step, finished_on])

        # Add current episode reward to total rewards list
        rewards_all_episodes.append(rewards_current_episode)
        if rewards_current_episode > max_reward:
            max_reward = rewards_current_episode
            save_output(q_table, prefix='max_reward')

    # Calculate and print the average reward per thousand episodes
    rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), _num_episodes / 500)
    count = 500

    # print("********Average reward per 500 hundred episodes********\n")
    squashed = []
    for r in rewards_per_thousand_episodes:
        #  print(count, ": ", str(sum(r / 500)))
        squashed.append(sum(r / 500))
        count += 500

    save_output(q_table)
    plot_it(squashed)

    print('Performance:', str(calc_performance(performance)))
    performance_output(performance)

def save_output(input_table, prefix=None):
    file_name = "q_table"
    if prefix:
        file_name = file_name + "_" + str(prefix)

    retval = []
    for idx, value in enumerate(input_table):
        temp = [*env.state_table[idx][0], *env.state_table[idx][1], *value]
        retval.append(temp)

    np.savetxt("../data/state_" + file_name + ".csv",
               retval,
               delimiter=", ",
               fmt='% s',
               header='AI L, AI R, O L, O R, swap, L L, L R, R R, R L')

    np.savetxt("../data/"+file_name + ".csv",
               input_table,
               delimiter=", ",
               fmt='% s')


def load_max_reward_q_table():
    file_exists = exists('../data/q_table_max_reward.csv')
    if file_exists:
        data = np.genfromtxt('../data/q_table_max_reward.csv', delimiter=',')
        return data
    else:
        return False


def plot_it(data):
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
    plt.title('Average reward per 500 episodes')

    # function to show the plot
    plt.savefig('../data/reward_vs_episode.png')
    plt.show()


def calc_performance(performance_data):
    wins = 0

    for p in performance_data:
        if p[4] == 'Draw' or p[4] == 'AI':
            wins += 1

    return wins / len(performance_data)


def performance_output(performance_data):
    np.savetxt("../data/raw_performance.csv",
               performance_data,
               delimiter=", ",
               fmt='% s',
               header='episode, exploration_rate, rewards_current_episode, step, winner')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q-algorithm arguments')
    parser.add_argument('--num_episodes', type=int, default=6000,
                        help='how many games to play')
    parser.add_argument('--max_steps_per_episode', type=int, default=50,
                        help='Number of turns to take in a game before starting a new game.')
    parser.add_argument('--learning_rate', type=float, default=0.1,
                        help='rate at which algorithm updates new q-values')
    parser.add_argument('--discount_rate', type=float, default=0.99,
                        help='used to weight the old and new q-values when updating q-table')
    parser.add_argument('--min_exploration_rate', type=float, default=0.01,
                        help='minimum value for exploration/exploitation ration can get')
    parser.add_argument('--exploration_decay_rate', type=float, default=0.001,
                        help='speed at which exploration rate reaches minimum exploration rate')
    parser.add_argument('--use_q_table_for_actions', type=bool, default=False,
                        help='If True the agent\'s opponent will use a previously saved q-table.  \
                        if False the agent\'s opponent will pick actions at random')
    args = parser.parse_args()

    main(num_episodes=args.num_episodes,
         max_steps_per_episode=args.max_steps_per_episode,
         learning_rate=args.learning_rate,
         discount_rate=args.discount_rate,
         min_exploration_rate=args.min_exploration_rate,
         exploration_decay_rate=args.exploration_decay_rate,
         use_q_table_for_actions=args.use_q_table_for_actions)

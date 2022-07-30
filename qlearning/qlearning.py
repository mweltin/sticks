"""
Implementation of a Q-Learning algorithm to learn to game of sticks
Author: Markus Weltin
"""
import argparse
from utilities.utility import Utility
import environment.env as env
import numpy as np
import random
import rules.rules as rules

parser = argparse.ArgumentParser(description='Process some integers.')


def main(
        num_episodes,
        max_steps_per_episode,
        learning_rate,
        discount_rate,
        min_exploration_rate,
        exploration_decay_rate,
        use_q_table_for_actions,
        skip_plot,
):
    utility = Utility("../data/qlearning")
    action_space_size = len(env.action_table)
    state_space_size = len(env.state_table)

    ''' initialize q-table with all zeros, i.e. no knowledge or load a previous good q-table'''
    q_table = utility.load_max_reward_q_table()
    if not isinstance(q_table, np.ndarray) or not use_q_table_for_actions:
        q_table = np.zeros((state_space_size, action_space_size))

    env.eliminate_invalid_actions(env.state_table, q_table)
    opponent_q_table = utility.load_max_reward_q_table()

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
        state_idx = env.reset()  # state is the index in the state_table
        rewards_current_episode = 0
        agent_first = True if random.uniform(0, 1) < 0.5 else False

        for step in range(_max_steps_per_episode):
            # Exploration-exploitation trade-off
            # Take new action
            # Update Q-table
            # Set new state
            # Add new reward
            if agent_first:
                q_table, done, state_idx, rewards_current_episode = utility.agents_turn(exploration_rate, q_table, state_idx,
                                                                                _learning_rate, _discount_rate,
                                                                                rewards_current_episode)

                if done:
                    finished_on = 'AI'
                    break

                # opponents turn
                state_idx, done = utility.dummy_turn(opponent_q_table, _use_q_table_for_actions, state_idx)

                if done:
                    finished_on = 'Opponent'
                    break

            else:
                # opponents turn
                state_idx, done = utility.dummy_turn(opponent_q_table, _use_q_table_for_actions, state_idx)

                if done:
                    finished_on = 'Opponent'
                    break

                q_table, done, state_idx, rewards_current_episode = utility.agents_turn(exploration_rate, q_table, state_idx,
                                                                                _learning_rate, _discount_rate,
                                                                                rewards_current_episode)
                if done:
                    finished_on = 'AI'
                    break

        # Exploration rate decay
        exploration_rate = _min_exploration_rate + \
                           (max_exploration_rate - _min_exploration_rate) * np.exp(-_exploration_decay_rate * episode)

        performance.append([episode, exploration_rate, rewards_current_episode, step, finished_on])

        # Add current episode reward to total rewards list
        rewards_all_episodes.append(rewards_current_episode)
        if rewards_current_episode > max_reward:
            max_reward = rewards_current_episode
            utility.save_output(q_table, prefix='max_reward')

    # Calculate and print the average reward per x episodes
    x = 100
    rewards_per_x_episodes = np.split(np.array(rewards_all_episodes), _num_episodes / x)
    count = x

    # print("********Average reward per 500 hundred episodes********\n")
    squashed = []
    for r in rewards_per_x_episodes:
        #  print(count, ": ", str(sum(r / 500)))
        squashed.append(sum(r / x))
        count += x

    utility.save_output(q_table)

    if not skip_plot:
        utility.plot_it(squashed, x)
    else:
        np.savetxt("../data/qlearning/reward_vs_episode.csv",
                   squashed,
                   delimiter=", ",
                   fmt='% s',
                   header='what')

    print('Performance:', str(utility.calc_performance(performance)))
    utility.performance_output(performance)


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
                        help='If True the agent and opponent will use a previously saved q-table.  \
                        if False the agent and opponent will with zeroed out q-table')
    parser.add_argument('--skip_plot', type=bool, default=False,
                        help='If True do not plot results.  Used when running qlearning algo multiple times times \
                             from the command line')
    args = parser.parse_args()

    main(num_episodes=args.num_episodes,
         max_steps_per_episode=args.max_steps_per_episode,
         learning_rate=args.learning_rate,
         discount_rate=args.discount_rate,
         min_exploration_rate=args.min_exploration_rate,
         exploration_decay_rate=args.exploration_decay_rate,
         use_q_table_for_actions=args.use_q_table_for_actions,
         skip_plot=args.skip_plot)

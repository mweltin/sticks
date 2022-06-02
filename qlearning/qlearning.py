"""
Implementation of a Q-Learning algorithm to learn to game of sticks
Author: Markus Weltin
"""
import numpy as np
import random
import environment.env as env
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')


def main(
        num_episodes=10000,
        max_steps_per_episode=75,
        learning_rate=0.1,
        discount_rate=0.99,
        min_exploration_rate=0.01,
        exploration_decay_rate=0.001,
):
    action_space_size = len(env.action_table)
    state_space_size = len(env.state_table)

    ''' initialize q-table with all zeros, i.e. no knowledge'''
    q_table = np.zeros((state_space_size, action_space_size))
    env.eliminate_invalid_actions(env.state_table, q_table)

    '''how many games to play'''
    _num_episodes = num_episodes
    ''' how many turns to take in a game before starting a new game. '''
    _max_steps_per_episode = max_steps_per_episode

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
    max_reward = 0

    # Q-learning algorithm
    for episode in range(_num_episodes):
        # initialize new episode params
        state_idx = env.reset()  # state is the index in the env.state_table
        done = False
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

            if done:
                rewards_current_episode += reward
                break

            q_table[state_idx][action] = q_table[state_idx][action] * (1 - _learning_rate) + \
                                         _learning_rate * (
                                                 reward + _discount_rate * np.nanargmax(q_table[new_state_idx]))

            state_idx = new_state_idx
            rewards_current_episode += reward

            # opponents turn
            action = env.select_random_action(state_idx, 1)
            new_state_idx, reward, done, info = env.step(state_idx, env.Players.opponent, action)
            state_idx = new_state_idx

            if done:
                break
        # Exploration rate decay
        exploration_rate = _min_exploration_rate + \
                           (max_exploration_rate - _min_exploration_rate) * np.exp(-_exploration_decay_rate * episode)
        # Add current episode reward to total rewards list
        rewards_all_episodes.append(rewards_current_episode)
        if rewards_current_episode > max_reward:
            max_reward = rewards_current_episode
            save_output(q_table, prefix='max_reward')

    # Calculate and print the average reward per thousand episodes
    rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), _num_episodes / 1000)
    count = 1000

    print("********Average reward per thousand episodes********\n")
    for r in rewards_per_thousand_episodes:
        print(count, ": ", str(sum(r / 1000)))
        count += 1000

    save_output(q_table)


def save_output(input_table, prefix=None):
    file_name = "q_table"
    if prefix:
        file_name = file_name + "_" + str(prefix)

    retval = []
    for idx, value in enumerate(input_table):
        temp = [*env.state_table[idx][0], *env.state_table[idx][1], *value]
        retval.append(temp)

    np.savetxt("state_" + file_name + ".csv",
               retval,
               delimiter=", ",
               fmt='% s',
               header='AI L, AI R, O L, O R, swap, L L, L R, R R, R L')

    np.savetxt(file_name + ".csv",
               input_table,
               delimiter=", ",
               fmt='% s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q-algorithm arguments')
    parser.add_argument('--num_episodes', type=int, default=60000,
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
    args = parser.parse_args()

    main(num_episodes=args.num_episodes,
         max_steps_per_episode=args.max_steps_per_episode,
         learning_rate=args.learning_rate,
         discount_rate=args.discount_rate,
         min_exploration_rate=args.min_exploration_rate,
         exploration_decay_rate=args.exploration_decay_rate)

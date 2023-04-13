"""
Implementation of a Q-Learning algorithm to learn to game of sticks
Author: Markus Weltin
"""

import argparse
from agent.player import Player
from agent.wolf_agent import Wolf as Agent
from utilities.utility import Utility
import environment.env as env
import numpy as np
import random

parser = argparse.ArgumentParser(description='Process some integers.')


def main(
        num_episodes,
        max_steps_per_episode,
        learning_rate_win,
        learning_rate_lose,
        discount_rate,
        min_exploration_rate,
        exploration_decay_rate,
        use_q_table_for_actions,
        skip_plot,
):

    wolf_a = Agent('wolf')
    winning_learning_rate = 0.05
    losing_learning_rate = 0.1

    wolf_a.winning_learning_rate = winning_learning_rate
    wolf_a.losing_learning_rate = losing_learning_rate

    dummy = Player(name='dummy', strategy='random', player_index=1)

    for episode in range(num_episodes):
        wolf_a.turn_counter = 0
        wolf_a.rewards_current_episode = 0
        finished_on = 'Draw'
        state_idx = env.reset()
        rewards_current_episode = 0
        agent_first = True if random.uniform(0, 1) < 0.5 else False

        for step in range(max_steps_per_episode):
            if agent_first:
                wolf_a.player_index = 0
                dummy.player_index = 1
                state_idx, reward, done, info  = wolf_a.take_turn(state_idx, episode)
                if done:
                    finished_on = wolf_a.name
                    wolf_a.win_counter += 1
                    break

                state_idx, reward, done, info = dummy.take_turn(state_idx)
                if done:
                    finished_on = dummy.name
                    break
            else:
                wolf_a.player_index = 1
                dummy.player_index = 0
                state_idx, reward, done, info = dummy.take_turn(state_idx)
                if done:
                    finished_on = dummy.name
                    break

                state_idx, reward, done, info = wolf_a.take_turn(state_idx, episode)
                if done:
                    finished_on = wolf_a.name
                    wolf_a.win_counter += 1
                    break

        if finished_on == 'Draw':
            wolf_a.win_counter += 1

        wolf_a.episode_data.append([episode, wolf_a.turn_counter, wolf_a.rewards_current_episode])

    wolf_a.save_output()
    wolf_a.save_it(wolf_a.episode_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q-algorithm arguments')
    parser.add_argument('--num_episodes', type=int, default=6000,
                        help='how many games to play')
    parser.add_argument('--max_steps_per_episode', type=int, default=50,
                        help='Number of turns to take in a game before starting a new game.')
    parser.add_argument('--learning_rate_win', type=float, default=0.0025,
                        help='rate at which algorithm updates new q-values')
    parser.add_argument('--learning_rate_lose', type=float, default=0.01,
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
         learning_rate_win=args.learning_rate_win,
         learning_rate_lose=args.learning_rate_lose,
         discount_rate=args.discount_rate,
         min_exploration_rate=args.min_exploration_rate,
         exploration_decay_rate=args.exploration_decay_rate,
         use_q_table_for_actions=args.use_q_table_for_actions,
         skip_plot=args.skip_plot
         )

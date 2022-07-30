from agent.agent import Agent
import argparse
import environment.env as env
import random


def main(num_episodes, max_steps_per_episode, skip_plot):
    agent_1 = Agent('agent_1')
    agent_2 = Agent('agent_2')

    for episode in range(num_episodes):
        finished_on = 'Draw'
        # initialize new episode params
        state_idx = env.reset()  # state is the index in the state_table
        rewards_current_episode = 0
        current_agent = agent_1 if random.uniform(0, 1) < 0.5 else agent_2
        other_agent = agent_1 if current_agent == agent_2 else agent_1

        if current_agent == agent_1:
            agent_1.player_index = 0
            agent_2.player_index = 1
        else:
            agent_1.player_index = 1
            agent_2.player_index = 0

        for step in range(max_steps_per_episode):
            state_idx, done = current_agent.take_turn(state_idx, episode)
            if done:
                finished_on = current_agent.name
                current_agent.win_counter += 1
                break
            current_agent = agent_1 if current_agent == agent_2 else agent_2
            state_idx, done = current_agent.take_turn(state_idx, episode)
            if done:
                finished_on = current_agent.name
                current_agent.win_counter += 1
                break

        if finished_on == 'Draw':
            current_agent.win_counter += 0.5
            other_agent.win_counter += 0.5

        if not episode % 500:
            agent_1.record_wins()
            agent_2.record_wins()

    agent_1.save_output()
    agent_2.save_output()

    if not skip_plot:
        agent_2.plot_it()
        agent_1.plot_it()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dual agent Q-algorithm arguments')
    parser.add_argument('--num_episodes', type=int, default=6000,
                        help='how many games to play')
    parser.add_argument('--max_steps_per_episode', type=int, default=50,
                        help='Number of turns to take in a game before starting a new game.')
    parser.add_argument('--skip_plot', type=bool, default=False,
                        help='If True do not plot results.  Used when running qlearning algo multiple times times \
                             from the command line')
    args = parser.parse_args()
    main(args.num_episodes, args.max_steps_per_episode, args.skip_plot)

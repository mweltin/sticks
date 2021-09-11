"""
My short cool script
Author: Cool Dude
"""
import numpy as np
import random
import environment.env as env


def main():
    action_space_size = env.action_space
    state_space_size = env.state_space

    q_table = np.zeros((state_space_size, action_space_size))
    num_episodes = 10000
    max_steps_per_episode = 100

    learning_rate = 0.1
    discount_rate = 0.99

    exploration_rate = 1
    max_exploration_rate = 1
    min_exploration_rate = 0.01
    exploration_decay_rate = 0.001

    rewards_all_episodes = []

    # Q-learning algorithm
    for episode in range(num_episodes):
        # initialize new episode params
        state = env.reset()
        done = False
        rewards_current_episode = 0

        for step in range(max_steps_per_episode):
            # Exploration-exploitation trade-off
            # Take new action
            # Update Q-table
            # Set new state
            # Add new reward
            exploration_rate_threshold = random.uniform(0, 1)
            if exploration_rate_threshold > exploration_rate:
                action = np.argmax(q_table[state, :])
            else:
                action = env.action_space.sample()

            new_state, reward, done, info = env.step(action)
            # Update Q-table for Q(s,a)
            q_table[state, action] = q_table[state, action] * (1 - learning_rate) + \
                                     learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))

            state = new_state
            rewards_current_episode += reward

            if done:
                break


        # Exploration rate decay
        exploration_rate = min_exploration_rate + \
                           (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)
        # Add current episode reward to total rewards list
        rewards_all_episodes.append(rewards_current_episode)

    # Calculate and print the average reward per thousand episodes
    rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), num_episodes / 1000)
    count = 1000

    print("********Average reward per thousand episodes********\n")
    for r in rewards_per_thousand_episodes:
        print(count, ": ", str(sum(r / 1000)))
        count += 1000



if __name__ == '__main__':
    main()

from agent.agent import Agent
import environment.env as env
from collections import namedtuple
import torch
import torch.nn as nn
import random
import torch.optim as optim
from dqn import DQN
from replay_memory import ReplayMemory
import numpy as np

"""
A Deep Q-Learning Agent is a modified Q-learning algorithm.
It replaces the Q-Table with a neural network to 
approximate an optimal policy. 
"""

class DeepQ(Agent):

    def __init__(self, name='name not set'):
        super(DeepQ, self).__init__(name)
        # Get number of actions
        n_actions = len(env.action_table)
        # Get the number of state observations
        state_idx = env.reset()
        state = env.state_to_tensor(state_idx)
        n_observations = len(state)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        Transition = namedtuple('Transition',
                                ('state', 'action', 'next_state', 'reward'))
        self.policy_net = DQN(n_observations, n_actions).to(self.device)
        target_net = DQN(n_observations, n_actions).to(self.device)
        BATCH_SIZE = 128
        GAMMA = 0.99
        TAU = 0.005
        LR = 1e-4
        optimizer = optim.AdamW(self.policy_net.parameters(), lr=LR, amsgrad=True)
        memory = ReplayMemory(10000)

        steps_done = 0

    def get_action(self, state_idx):
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > self.exploration_rate:
            with torch.no_grad():
                # t.max(1) will return the largest column value of each row.
                # second column on max result is index of where max element was
                # found, so we pick action with the larger expected reward.
                state_tensor = torch.tensor(np.array([env.state_to_tensor(state_idx)]), device=self.device,
                                            dtype=torch.float32)
                action = self.policy_net(state_tensor).max(1)[1].view(1, 1)
                return action
        else:
            action = env.select_random_action(state_idx, self.player_index)
            return torch.tensor([[action]], device=self.device, dtype=torch.long)

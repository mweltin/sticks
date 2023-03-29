from agent.agent import Agent
import environment.env as env
from collections import namedtuple
import torch
import torch.nn as nn
import random
import torch.optim as optim
from dqn import DQN
from replay_memory import ReplayMemory
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
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        Transition = namedtuple('Transition',
                                ('state', 'action', 'next_state', 'reward'))
        policy_net = DQN(n_observations, n_actions).to(device)
        target_net = DQN(n_observations, n_actions).to(device)
        BATCH_SIZE = 128
        GAMMA = 0.99
        self.epsilon_start = 0.9
        EPS_END = 0.05
        EPS_DECAY = 1000
        TAU = 0.005
        LR = 1e-4
        optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
        memory = ReplayMemory(10000)

        steps_done = 0

    def get_action(state_idx, player_index=0):
        global steps_done
        sample = random.random()
        eps_threshold = EPS_END + (EPS_START - EPS_END) * \
                        math.exp(-1. * steps_done / EPS_DECAY)
        steps_done += 1
        if sample > eps_threshold:
            with torch.no_grad():
                # t.max(1) will return the largest column value of each row.
                # second column on max result is index of where max element was
                # found, so we pick action with the larger expected reward.
                state_tensor = torch.tensor(np.array([env.state_to_tensor(state_idx)]), device=device,
                                            dtype=torch.float32)
                action = policy_net(state_tensor).max(1)[1].view(1, 1)
                return action
        else:
            action = env.select_random_action(state_idx, player_index)
            return torch.tensor([[action]], device=device, dtype=torch.long)

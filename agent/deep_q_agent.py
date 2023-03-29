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

        self.transition = namedtuple('Transition',
                                ('state', 'action', 'next_state', 'reward'))
        self.policy_net = DQN(n_observations, n_actions).to(self.device)
        self.target_net = DQN(n_observations, n_actions).to(self.device)
        self.batch_size = 128
        self.gamma = 0.99
        TAU = 0.005
        LR = 1e-4
        self.optimizer = optim.AdamW(self.policy_net.parameters(), lr=LR, amsgrad=True)
        self.memory = ReplayMemory(10000)

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

    def take_turn(self, state_index, episode):
        action = self.get_action(state_index)
        new_state_idx, reward, done, info = env.step(state_index, self.player_index, action)


        self.update_q_table(state_index, new_state_idx, reward, done, action)


        self.exploration_rate = self._min_exploration_rate + (
                self.max_exploration_rate - self._min_exploration_rate) * np.exp(
            -self._exploration_decay_rate * episode)
        return new_state_idx, done

    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return
        transitions = self.memory.sample(self.batch_size)
        # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
        # detailed explanation). This converts batch-array of Transitions
        # to Transition of batch-arrays.
        batch = self.transition(*zip(*transitions))

        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                                batch.next_state)), device=self.device, dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state
                                           if s is not None])
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1)[0].
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(self.batch_size, device=self.device)
        with torch.no_grad():
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0]
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * self.gamma) + reward_batch

        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        # In-place gradient clipping
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.optimizer.step()

    def neural_net_to_q_table(self):
        """output a newural net to be used by a Player class object """
        pass

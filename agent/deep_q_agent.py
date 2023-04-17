import environment.env as env
from collections import namedtuple
import torch
import torch.nn as nn
import random
import torch.optim as optim
import numpy as np
from deep_q.replay_memory import ReplayMemory
from deep_q.deep_q_network import DQN

from agent.agent import Agent
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
        self.state_idx = env.reset()
        self.state = env.state_to_ndarray(self.state_idx)
        n_observations = len(self.state)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.transition = namedtuple('Transition',
                                     ('state', 'action', 'next_state', 'reward'))
        self.policy_net = DQN(n_observations, n_actions).to(self.device)
        self.target_net = DQN(n_observations, n_actions).to(self.device)
        self.batch_size = 128
        self.gamma = 0.99
        self.tau = 0.005
        self.learning_rate = 1e-4
        self.optimizer = optim.AdamW(self.policy_net.parameters(), lr=self.learning_rate, amsgrad=True)
        self.memory = ReplayMemory(10000)


    def get_action(self, state_idx):
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > self.exploration_rate:
            with torch.no_grad():
                # t.max(1) will return the largest column value of each row.
                # second column on max result is index of where max element was
                # found, so we pick action with the larger expected reward.
                state_tensor = torch.tensor(np.array([env.state_to_ndarray(state_idx)]), device=self.device,
                                            dtype=torch.float32)
                action = self.policy_net(state_tensor).max(1)[1].view(1, 1)
                return action
        else:
            action = env.select_random_action(state_idx, self.player_index)
            return torch.tensor([[action]], device=self.device, dtype=torch.long)

    def take_turn(self, state_index, episode, step):
        self.turn_counter += 1
        state = torch.tensor(env.state_to_ndarray(state_index), dtype=torch.float32, device=self.device).unsqueeze(0)

        action = self.get_action(state_index)
        observation, reward, terminated, info = env.step(state_index, self.player_index, action.item())
        reward = reward / (1 + step)
        self.rewards_current_episode += reward
        reward = torch.tensor([reward], device=self.device)
        done = terminated  # @todo or truncated SEE ORIGINAL CODE TRUNCATED IS?

        if terminated:
            next_state = None
        else:
            next_state = torch.tensor(env.state_to_ndarray(observation), dtype=torch.float32,
                                      device=self.device).unsqueeze(0)

        # Store the transition in memory
        self.memory.push(state, action, next_state, reward)

        # Move to the next state
        self.state = next_state
        self.state_idx = observation

        # Perform one step of the optimization (on the policy network)
        self.optimize_model()

        # Soft update of the target network's weights
        # θ′ ← τ θ + (1 −τ )θ′
        target_net_state_dict = self.target_net.state_dict()
        policy_net_state_dict = self.policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key] * self.tau + target_net_state_dict[key] * (
                        1 - self.tau)
        self.target_net.load_state_dict(target_net_state_dict)

        self.exploration_rate = self._min_exploration_rate + (
                self.max_exploration_rate - self._min_exploration_rate) * np.exp(
            -self._exploration_decay_rate * episode)

        return self.state_idx, reward, done, info

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

    def save_output(self, prefix=None):
        file_name = "q_table"
        q_table_with_state = []
        q_table = []

        if prefix:
            file_name = file_name + "_" + str(prefix)

        for idx, value in enumerate(env.state_table):
            input_array = env.state_to_ndarray(idx)
            network_input = torch.tensor(input_array, device=self.device, dtype=torch.float32)
            temp = [*env.state_table[idx][0], *env.state_table[idx][1], *self.policy_net.forward(network_input).tolist()]
            q_table_with_state.append(temp)
            q_table.append(self.policy_net.forward(network_input).tolist())

        np.savetxt(self.utility.base_directory + "/state_" + file_name + ".csv",
                   q_table_with_state,
                   delimiter=", ",
                   fmt='% s',
                   header='AI L, AI R, O L, O R, swap, L L, L R, R R, R L')

        np.savetxt(self.utility.base_directory + "/" + file_name + ".csv",
                   q_table,
                   delimiter=", ",
                   fmt='% s')

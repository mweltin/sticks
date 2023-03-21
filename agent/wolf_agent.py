from agent.agent import Agent
import environment.env as env

"""
A Wolf Agent is a modified Q-learning algorithm. 
Characterized by a strategy with a variable learning rate.
The lerning rate fluctuates between at a frequency related to its 
win / loss rate. 
"""
class Wolf(Agent):

    def __init__(self, name='name not set'):
        super(Wolf,self).__init__(name)
        self._policy = None
        self._average_policy = None
        self._winning_learning_rate = 0.05
        self._losing_learning_rate = 0.1
        self.learning_rate = self._winning_learning_rate
        self.counter = 0
        self.init_policy_table()
        self.init_average_policy_table()

    def init_policy_table(self):
        self._policy =self.get_q_table().copy()
        self._policy += 1/len(env.action_table)
        return

    def init_average_policy_table(self):
        self._average_policy =self.get_q_table().copy()
        return

    def set_winning_learning_rate(self, value):
        self._winning_learning_rate = value

    def get_winning_learning_rate(self):
        return self._winning_learning_rate

    winning_learning_rate = property(get_winning_learning_rate, set_winning_learning_rate)

    def set_losing_learning_rate(self, value):
        self._losing_learning_rate = value

    def get_losing_learning_rate(self):
        return self._losing_learning_rate

    losing_learning_rate = property(get_losing_learning_rate, set_losing_learning_rate)

    def take_turn(self, state_index, episode):
        new_state_idx, done = super(Wolf, self).take_turn(state_index, episode)
        self.counter += 1 # this needs to be called before update_average_policy
        self.update_policy(state_index)
        self.update_average_policy(state_index)
        self.update_learning_rate(state_index)
        return new_state_idx, done

    def update_policy(self, state_index):
        # pi(s,a') = pi(s,a') + learning_rate if a' = max of Q(s,:)
        # pi(s,a') = pi(s,a') + -learning_rate/(A_i - 1) where A_i is the number of actions the agent can take
        q_arg_max = env.nanargmax_unbiased(self._q_table[state_index])
        A_i = len(self._policy[state_index])
        for action in range(len(self._policy[state_index])):
            if action == q_arg_max:
                self._policy[state_index][action] = self.learning_rate
            else:
                self._policy[state_index][action] = -self.learning_rate/(A_i-1) + self._policy[state_index][action]
        return

    def update_average_policy(self, state_index):
        # pi_avg(s,a') = pi_avg(s,a') + (pi(s,a') - pi_avg(s,a'))/counter
        #where a' = for every a' that is an element of A_i
        # A_i is the ith agent in a multi agent environment
        for action in range(len(self._average_policy[state_index])):
            self._average_policy[state_index][action] = self._average_policy[state_index][action] + \
                (self._policy[state_index][action]  - self._average_policy[state_index][action] )/self.counter
        return

    def update_learning_rate(self, state_index):
        pi_avg_total = 0
        pi_total = 0
        for action in range( len(env.action_table) ):
            pi_avg_total += self._q_table[state_index][action] * self._average_policy[state_index][action]
            pi_total += self._q_table[state_index][action] * self._policy[state_index][action]

        # if SUM( pi(s,a)*Q(s,a) ) for all a is greater than Sum( pi_avg(s,a)*Q(s,a))
        # we use the winning rate
        # otherwise we use the losing rate
        if pi_total > pi_avg_total:
            self.learning_rate = self.winning_learning_rate
        else:
            self.learning_rate = self.losing_learning_rate



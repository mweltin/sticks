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
        super().__init__(name)
        self._policy = None
        self._average_policy = None
        self._winning_learning_rate = 0.05
        self._losing_learning_rate = 0.1
        self.init_policy_table()
        self.init_average_policy_table()

    def init_policy_table(self):
        self._average_policy =self.get_q_table().copy()
        self._average_policy += 1/len(env.action_table)
        return

    def init_average_policy_table(self):
        self._policy = self.get_q_table().copy()
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

import environment.env as env
import unittest


class EnvironmentTestCase(unittest.TestCase):
    def test_rest_function_gives_correct_state(self):
        reset_index = env.reset()
        self.assertEqual([[1, 1], [1, 1]], env.state_table[reset_index])

    def test_select_random_action(self):
        state_index = env.reset()  # only four actions are allowed in this state
        active_player_index = 0
        action = env.select_random_action(state_index, active_player_index)
        self.assertIn(action, [3, 4, 2, 1])

    def test_will_lose_next_step(self):
        state = [[0, 1], [4, 0]]
        will_lose = env.will_lose_next_step(state)
        self.assertTrue(will_lose)

        state = [[2, 0], [3, 0]]
        will_lose = env.will_lose_next_step(state)
        self.assertTrue(will_lose)

        state = [[2, 0], [4, 0]]
        will_lose = env.will_lose_next_step(state)
        self.assertFalse(will_lose)

    def test_will_win_in_two_steps(self):
        state = [[3, 0], [1, 0]]
        will_win = env.will_win_in_two_steps(state)
        self.assertTrue(will_win)

        state = [[0, 1], [2, 0]]
        will_win = env.will_win_in_two_steps(state)
        self.assertTrue(will_win)

    def test_reward_when_agent_won(self):
        state_agent_is_winner = [[1, 0], [0, 0]]
        reward = env.get_reward(state_agent_is_winner)
        self.assertEqual(100, reward)

    def test_reward_when_opponent_won(self):
        state_agent_is_winner = [[0, 0], [4, 0]]
        reward = env.get_reward(state_agent_is_winner)
        self.assertEqual(-100, reward)

    def test_reward_when_agent_is_close_to_winning(self):
        state_agent_is_winner = [[3, 0], [1, 0]]
        reward = env.get_reward(state_agent_is_winner)
        self.assertEqual(50, reward)

    def test_reward_when_agent_is_close_to_losing(self):
        state_agent_is_winner = [[1, 0], [4, 0]]
        reward = env.get_reward(state_agent_is_winner)
        self.assertEqual(-50, reward)

    def test_reward_regular_case(self):
        state_agent_is_winner = [[1, 2], [3, 1]]
        reward = env.get_reward(state_agent_is_winner)
        self.assertEqual(-1, reward)

    def test_select_random_action_when_only_one_valid_action_exists(self):
        test_state = [[1, 0], [1, 0]]
        state_index = env.state_table.index(test_state)
        action = env.select_random_action(state_index, 0)
        self.assertEqual(1, action)

    def test_select_random_action_when_only_swap_and_one_other_action_exists(self):
        test_state = [[4, 0], [1, 0]]
        state_index = env.state_table.index(test_state)
        action = env.select_random_action(state_index, 0)
        self.assertIn(action, [1, 0])

    def test_eliminate_invalid_actions(self):
        q_table = [[0, 0, 0, 0, 0]]
        state = [[[1, 0], [1, 0]]]
        env.eliminate_invalid_actions(state, q_table)
        self.assertEqual([[None, 0, None, None, None]], q_table)

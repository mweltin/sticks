import rules.rules as rules
import environment.env as env
import unittest


class RulesTestCase(unittest.TestCase):

    def test_has_winner_opponent_wins(self):
        value = [[0, 0], [0, 1]]
        act = rules.has_winner(value)
        self.assertEqual(env.Players.opponent, act)

    def test_has_winner_when_agent_wins(self):
        value = [[1, 0], [0, 0]]
        act = rules.has_winner(value)
        self.assertEqual(env.Players.agent, act)

    def test_has_winner_when_there_is_no_winner(self):
        value = [[1, 0], [0, 1]]
        act = rules.has_winner(value)
        self.assertFalse(act)
        self.assertNotEqual(act, env.Players.agent)

    def test_can_swap_returns_true_if_one_hand_is_empty_and_the_other_has_and_even_number(self):
        value = [0, 2]
        act = rules.can_swap(value)
        self.assertTrue(act)

    def test_can_swap_false_if_one_hand_is_empty_and_the_other_has_and_odd_number(self):
        value = [0, 3]
        act = rules.can_swap(value)
        self.assertFalse(act)

    def test_can_swap_false_if_both_hands_are_not_empty(self):
        value = [1, 3]
        act = rules.can_swap(value)
        self.assertFalse(act)

    def test_swap_returns_an_array_of_two_elements_and_both_elements_are_half_of_largest_element_in_input_array(self):
        val = 4
        value = [0, val]
        act = rules.swap(value)
        self.assertEqual([val / 2, val / 2], act)

    def test_get_opponent_player_index(self):
        active_player_index = 0
        opponent_index = rules.get_opponent_player_index(active_player_index)
        self.assertEqual(1, opponent_index)
        active_player_index = 1
        opponent_index = rules.get_opponent_player_index(active_player_index)
        self.assertEqual(0, opponent_index)

    def test_take_turn_allows_for_swap(self):
        state = [[0, 4], [1, 1]]
        active_player_index = 0
        action = env.action_table[0]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual([2, 2], new_state[active_player_index])

    def test_take_turn_handles_left_to_left_for_both_players(self):
        state = [[2, 1], [1, 2]]
        expected_state = [[2, 1], [3, 2]]
        active_player_index = 0
        action = env.action_table[1]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual(expected_state, new_state)

        state = [[2, 1], [1, 2]]
        expected_state = [[3, 1], [1, 2]]
        active_player_index = 1
        action = env.action_table[1]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual(expected_state, new_state)

    def test_take_turn_handles_left_to_right_for_both_players(self):
        state = [[2, 1], [1, 2]]
        expected_state = [[2, 1], [1, 4]]
        active_player_index = 0
        action = env.action_table[2]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual(expected_state, new_state)

        state = [[2, 1], [1, 2]]
        expected_state = [[2, 2], [1, 2]]
        active_player_index = 1
        action = env.action_table[2]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual(expected_state, new_state)

    def test_take_turn_handles_right_to_left_for_both_players(self):
        state = [[2, 1], [1, 2]]
        expected_state = [[2, 1], [2, 2]]
        active_player_index = 0
        action = env.action_table[4]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual(expected_state, new_state)

        state = [[2, 1], [1, 2]]
        expected_state = [[4, 1], [1, 2]]
        active_player_index = 1
        action = env.action_table[4]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual(expected_state, new_state)

    def test_take_turn_handles_right_to_right_for_both_players(self):
        state = [[2, 1], [1, 2]]
        expected_state = [[2, 1], [1, 3]]
        active_player_index = 0
        action = env.action_table[3]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual(expected_state, new_state)

        state = [[2, 1], [1, 2]]
        expected_state = [[2, 3], [1, 2]]
        active_player_index = 1
        action = env.action_table[3]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual(expected_state, new_state)

    def test_take_turn_handles_case_when_outcome_is_above_five(self):
        state = [[4, 1], [1, 4]]
        expected_state = [[4, 1], [1, 3]]
        active_player_index = 0
        action = env.action_table[2]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual(expected_state, new_state)

    def test_take_turn_handles_case_when_outcome_is_equal_five(self):
        state = [[4, 1], [1, 1]]
        expected_state = [[4, 1], [1, 0]]
        active_player_index = 0
        action = env.action_table[2]
        new_state = rules.take_turn(state, active_player_index, action)
        self.assertEqual(expected_state, new_state)

    def test_get_valid_actions_identifies_when_swap_is_valid(self):
        state = [[4, 0], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertIn(env.action_table.index([env.Actions.SWAP]), valid_moves)

        state = [[4, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn(env.action_table.index([env.Actions.SWAP]), valid_moves)

    def test_get_valid_actions_identifies_when_right_right_is_valid(self):
        state = [[4, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertTrue(env.action_table.index([env.Actions.RIGHT, env.Actions.RIGHT]), valid_moves)

    def test_get_valid_actions_identifies_when_right_right_is_not_valid(self):
        state = [[4, 1], [1, 0]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn(env.action_table.index([env.Actions.RIGHT, env.Actions.RIGHT]), valid_moves)

        state = [[4, 0], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn(env.action_table.index([env.Actions.RIGHT, env.Actions.RIGHT]), valid_moves)

    def test_get_valid_actions_identifies_when_right_left_is_valid(self):
        state = [[4, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertIn(env.action_table.index([env.Actions.RIGHT, env.Actions.LEFT]), valid_moves)

    def test_get_valid_actions_identifies_when_right_left_is_not_valid(self):
        state = [[4, 0], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn(env.action_table.index([env.Actions.RIGHT, env.Actions.LEFT]), valid_moves)

        state = [[4, 1], [0, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn(env.action_table.index([env.Actions.RIGHT, env.Actions.LEFT]), valid_moves)

    def test_get_valid_actions_identifies_when_left_left_is_valid(self):
        state = [[4, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertIn(env.action_table.index([env.Actions.LEFT, env.Actions.LEFT]), valid_moves)

    def test_get_valid_actions_identifies_when_left_left_is_not_valid(self):
        state = [[4, 1], [0, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn(env.action_table.index([env.Actions.LEFT, env.Actions.LEFT]), valid_moves)

        state = [[0, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn(env.action_table.index([env.Actions.LEFT, env.Actions.LEFT]), valid_moves)

    def test_get_valid_actions_identifies_when_left_right_is_valid(self):
        state = [[4, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertIn(env.action_table.index([env.Actions.LEFT, env.Actions.RIGHT]), valid_moves)

    def test_get_valid_actions_identifies_when_left_right_is_not_valid(self):
        state = [[4, 1], [3, 0]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn(env.action_table.index([env.Actions.LEFT, env.Actions.RIGHT]), valid_moves)

        state = [[0, 2], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn(env.action_table.index([env.Actions.LEFT, env.Actions.RIGHT]), valid_moves)


if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()

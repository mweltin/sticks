import rules.rules as rules
import environment.env as env
import unittest


class RulesTestCase(unittest.TestCase):
    def test_when_player_one_wins_is_done_return_one(self):
        value = [[0, 0], [0, 1]]
        act = rules.is_done(value)
        self.assertEqual(1, act)

    def test_when_player_two_wins_is_done_return_two(self):
        value = [[1, 0], [0, 0]]
        act = rules.is_done(value)
        self.assertEqual(2, act)

    def test_when_there_is_no_winner_is_done_returns_zero(self):
        value = [[1, 0], [0, 1]]
        act = rules.is_done(value)
        self.assertEqual(0, act)

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
        new_state = rules.take_turn(state, active_player_index, 1, 1, True)
        self.assertEqual([2, 2], new_state[active_player_index])

    def test_take_turn_handles_left_to_left_for_both_players(self):
        state = [[2, 1], [1, 2]]
        expected_state = [[2, 1], [3, 2]]
        active_player_index = 0
        new_state = rules.take_turn(state, active_player_index, env.Actions.LEFT, env.Actions.LEFT)
        self.assertEqual(expected_state, new_state)

        state = [[2, 1], [1, 2]]
        expected_state = [[3, 1], [1, 2]]
        active_player_index = 1
        new_state = rules.take_turn(state, active_player_index, env.Actions.LEFT, env.Actions.LEFT)
        self.assertEqual(expected_state, new_state)

    def test_take_turn_handles_left_to_right_for_both_players(self):
        state = [[2, 1], [1, 2]]
        expected_state = [[2, 1], [1, 4]]
        active_player_index = 0
        new_state = rules.take_turn(state, active_player_index, env.Actions.LEFT, env.Actions.RIGHT)
        self.assertEqual(expected_state, new_state)

        state = [[2, 1], [1, 2]]
        expected_state = [[2, 2], [1, 2]]
        active_player_index = 1
        new_state = rules.take_turn(state, active_player_index, env.Actions.LEFT, env.Actions.RIGHT)
        self.assertEqual(expected_state, new_state)

    def test_take_turn_handles_right_to_left_for_both_players(self):
        state = [[2, 1], [1, 2]]
        expected_state = [[2, 1], [2, 2]]
        active_player_index = 0
        new_state = rules.take_turn(state, active_player_index, env.Actions.RIGHT, env.Actions.LEFT)
        self.assertEqual(expected_state, new_state)

        state = [[2, 1], [1, 2]]
        expected_state = [[4, 1], [1, 2]]
        active_player_index = 1
        new_state = rules.take_turn(state, active_player_index, env.Actions.RIGHT, env.Actions.LEFT)
        self.assertEqual(expected_state, new_state)

    def test_take_turn_handles_right_to_right_for_both_players(self):
        state = [[2, 1], [1, 2]]
        expected_state = [[2, 1], [1, 3]]
        active_player_index = 0
        new_state = rules.take_turn(state, active_player_index, env.Actions.RIGHT, env.Actions.RIGHT)
        self.assertEqual(expected_state, new_state)

        state = [[2, 1], [1, 2]]
        expected_state = [[2, 3], [1, 2]]
        active_player_index = 1
        new_state = rules.take_turn(state, active_player_index, env.Actions.RIGHT, env.Actions.RIGHT)
        self.assertEqual(expected_state, new_state)

    def test_take_turn_handles_case_when_outcome_is_above_five(self):
        state = [[4, 1], [1, 4]]
        expected_state = [[4, 1], [1, 3]]
        active_player_index = 0
        new_state = rules.take_turn(state, active_player_index, env.Actions.LEFT, env.Actions.RIGHT)
        self.assertEqual(expected_state, new_state)

    def test_take_turn_handles_case_when_outcome_is_equal_five(self):
        state = [[4, 1], [1, 1]]
        expected_state = [[4, 1], [1, 0]]
        active_player_index = 0
        new_state = rules.take_turn(state, active_player_index, env.Actions.LEFT, env.Actions.RIGHT)
        self.assertEqual(expected_state, new_state)

    def test_get_valid_actions_identifies_when_swap_is_valid(self):
        state = [[4, 0], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertIn('swap', valid_moves)

        state = [[4, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn('swap', valid_moves)

    def test_get_valid_actions_identifies_when_right_right_is_valid(self):
        state = [[4, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertTrue('right_right', valid_moves)

    def test_get_valid_actions_identifies_when_right_right_is_not_valid(self):
        state = [[4, 1], [1, 0]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn('right_right', valid_moves)

        state = [[4, 0], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn('right_right', valid_moves)

    def test_get_valid_actions_identifies_when_right_left_is_valid(self):
        state = [[4, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertIn('right_left', valid_moves)

    def test_get_valid_actions_identifies_when_right_left_is_not_valid(self):
        state = [[4, 0], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn('right_left', valid_moves)

        state = [[4, 1], [0, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn('right_left', valid_moves)

    def test_get_valid_actions_identifies_when_left_left_is_valid(self):
        state = [[4, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertIn('left_left', valid_moves)

    def test_get_valid_actions_identifies_when_left_left_is_not_valid(self):
        state = [[4, 1], [0, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn('left_left', valid_moves)

        state = [[0, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn('left_left', valid_moves)

    def test_get_valid_actions_identifies_when_left_right_is_valid(self):
        state = [[4, 1], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertIn('left_right', valid_moves)

    def test_get_valid_actions_identifies_when_left_right_is_not_valid(self):
        state = [[4, 1], [3, 0]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn('left_right', valid_moves)

        state = [[0, 2], [1, 1]]
        active_player_index = 0
        valid_moves = rules.get_valid_actions(state, active_player_index)
        self.assertNotIn('left_right', valid_moves)


if __name__ == '__main__':
    unittest.main()

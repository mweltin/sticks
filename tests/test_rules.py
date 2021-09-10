import rules.rules as rules
import unittest


class RulesTestCase(unittest.TestCase):
    def test_when_player_one_wins_is_done_return_one(self):
        value = [[0, 0], [0, 1]]
        act = rules.is_done(value)
        self.assertEqual(act, 1)

    def test_when_player_two_wins_is_done_return_two(self):
        value = [[1, 0], [0, 0]]
        act = rules.is_done(value)
        self.assertEqual(act, 2)

    def test_when_there_is_no_winner_is_done_returns_zero(self):
        value = [[1, 0], [0, 1]]
        act = rules.is_done(value)
        self.assertEqual(act, 0)

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
        self.assertEqual(act, [val/2, val/2])

    def test_take_turn_allows_for_swap(self):
        self.assertFalse(True)


if __name__ == '__main__':
    unittest.main()

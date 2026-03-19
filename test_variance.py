import unittest
from unittest.mock import patch
import io
import sys
from variance import _find_variance, find_variance_from_user_input, MAX_SCORE_COUNT, MAX_SCORE

class TestVariance(unittest.TestCase):

    def test_find_variance_normal_case(self):
        scores = [85, 87, 88, 89, 90]
        expected_variance = 2.96  # Correct calculation
        result = _find_variance(scores)
        self.assertAlmostEqual(result, expected_variance, places=2)

    def test_find_variance_single_score(self):
        scores = [85]
        result = _find_variance(scores)
        self.assertEqual(result, 0.0)

    def test_find_variance_identical_scores(self):
        scores = [90, 90, 90]
        result = _find_variance(scores)
        self.assertEqual(result, 0.0)

    def test_find_variance_empty_list(self):
        with self.assertRaises(ValueError) as cm:
            _find_variance([])
        self.assertEqual(str(cm.exception), "scores must not be empty")

    def test_find_variance_not_a_list(self):
        with self.assertRaises(TypeError) as cm:
            _find_variance("not a list")
        self.assertIn("scores must be a list", str(cm.exception))

    def test_find_variance_non_int_elements(self):
        with self.assertRaises(TypeError) as cm:
            _find_variance([85, 87.5, 88])
        self.assertEqual(str(cm.exception), "All scores must be integers (bool is not allowed)")

    def test_find_variance_bool_elements(self):
        with self.assertRaises(TypeError) as cm:
            _find_variance([85, True, 88])
        self.assertEqual(str(cm.exception), "All scores must be integers (bool is not allowed)")

    def test_find_variance_negative_scores(self):
        # Function allows negative, but in context scores are 0-100
        scores = [-10, 0, 10]
        result = _find_variance(scores)
        # Mean = 0, variance = (100 + 0 + 100)/3 ≈ 66.67
        self.assertAlmostEqual(result, 66.67, places=2)

    @patch('builtins.input', side_effect=['85,87,88'])
    def test_find_variance_from_user_input_valid(self, mock_input):
        result = find_variance_from_user_input()
        expected_variance = 1.5555555555555556  # Correct calculation for [85,87,88]
        self.assertAlmostEqual(result, expected_variance, places=2)

    @patch('builtins.input', side_effect=['85,87,88,89', '85,87,88'])
    @patch('builtins.print')
    def test_find_variance_from_user_input_too_many_scores(self, mock_print, mock_input):
        result = find_variance_from_user_input()
        expected = _find_variance([85, 87, 88])
        self.assertAlmostEqual(result, expected, places=2)
        # Check that the error message was printed for too many scores
        mock_print.assert_any_call("Only 3 scores are allowed.")

    @patch('builtins.input', side_effect=['85,87,88'])
    def test_get_scores_from_user_valid(self, mock_input):
        from variance import _get_scores_from_user
        result = _get_scores_from_user()
        self.assertEqual(result, [85, 87, 88])

    @patch('builtins.input', side_effect=['85,abc,88', '85,87,88'])
    @patch('builtins.print')
    def test_get_scores_from_user_invalid_int(self, mock_print, mock_input):
        from variance import _get_scores_from_user
        result = _get_scores_from_user()
        self.assertEqual(result, [85, 87, 88])
        mock_print.assert_called_with("Invalid input — please enter integers only, separated by commas.")

    @patch('builtins.input', side_effect=['85,87,88,89', '85,87,88'])
    @patch('builtins.print')
    def test_get_scores_from_user_too_many(self, mock_print, mock_input):
        from variance import _get_scores_from_user
        result = _get_scores_from_user()
        self.assertEqual(result, [85, 87, 88])
        mock_print.assert_called_with(f"Only {MAX_SCORE_COUNT} scores are allowed.")

    @patch('builtins.input', side_effect=['-5,87,88', '85,87,88'])
    @patch('builtins.print')
    def test_get_scores_from_user_out_of_range(self, mock_print, mock_input):
        from variance import _get_scores_from_user
        result = _get_scores_from_user()
        self.assertEqual(result, [85, 87, 88])
        mock_print.assert_called_with("Scores must be between 0 and 100 inclusive.")

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch

from src.cache_object import AlertCache


class TestAlertCache(unittest.TestCase):

    def test_current_week_returns_tuple(self):
        """Test that current_week returns a tuple (year, week)."""
        result = AlertCache.current_week()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], int)
        self.assertIsInstance(result[1], int)

    @patch.object(AlertCache, "current_week")
    def test_reset_week_new_week_detected(self, mock_current_week):
        """Test reset_week() resets threshold when a new week starts."""
        cache = AlertCache()
        cache.last_threshold = 50
        cache.last_week = (2025, 40)

        mock_current_week.return_value = (2025, 41)

        with patch("builtins.print") as mock_print:
            cache.reset_week()

        mock_print.assert_called_once_with("New week detected, resetting last threshold")
        self.assertEqual(cache.last_week, (2025, 41))
        self.assertIsNone(cache.last_threshold)

    @patch.object(AlertCache, "current_week")
    def test_reset_week_same_week_no_reset(self, mock_current_week):
        """Test reset_week() does nothing if same week."""
        cache = AlertCache()
        cache.last_threshold = 100
        cache.last_week = (2025, 40)

        mock_current_week.return_value = (2025, 40)

        with patch("builtins.print") as mock_print:
            cache.reset_week()

        mock_print.assert_not_called()
        self.assertEqual(cache.last_threshold, 100)
        self.assertEqual(cache.last_week, (2025, 40))


if __name__ == "__main__":
    unittest.main()

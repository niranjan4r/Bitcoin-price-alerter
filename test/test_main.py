import unittest
from unittest.mock import patch, MagicMock

import yaml

from src import main


class TestMain(unittest.TestCase):

    @patch("main.send_email")
    @patch("main.get_btc_data")
    @patch("main.AlertCache")
    @patch("main.time.sleep", return_value=None)
    def test_main_threshold_trigger(
            self, mock_sleep, mock_alert_cache, mock_get_btc_data, mock_send_email
    ):
        """Test case when BTC price drop crosses a threshold and email is sent."""

        config_data = {
            "interval_minutes": 1,
            "alert_threshold_percent": [5, 10, 20],
            "email": {
                "is_feature_enabled": True,
                "to": "test@example.com",
            },
        }

        mock_open = unittest.mock.mock_open(read_data=yaml.safe_dump(config_data))
        with patch("builtins.open", mock_open):
            mock_cache_instance = MagicMock()
            mock_cache_instance.last_threshold = 0
            mock_alert_cache.return_value = mock_cache_instance

            mock_get_btc_data.return_value = {"price": 50000, "ath": 100000}

            def stop_loop(_):
                raise SystemExit

            mock_sleep.side_effect = stop_loop

            with self.assertRaises(SystemExit):
                main.main()

        mock_get_btc_data.assert_called_once()
        mock_send_email.assert_called_once()
        mock_cache_instance.reset_week.assert_called_once()
        self.assertGreater(mock_cache_instance.last_threshold, 0)

    @patch("main.send_email")
    @patch("main.get_btc_data")
    @patch("main.AlertCache")
    @patch("main.time.sleep", return_value=None)
    def test_main_no_threshold_breach(
            self, mock_sleep, mock_alert_cache, mock_get_btc_data, mock_send_email
    ):
        """Test case when no threshold is breached and no email is sent."""

        config_data = {
            "interval_minutes": 1,
            "alert_threshold_percent": [5, 10, 20],
            "email": {
                "is_feature_enabled": True,
                "to": "test@example.com",
            },
        }

        mock_open = unittest.mock.mock_open(read_data=yaml.safe_dump(config_data))
        with patch("builtins.open", mock_open):
            mock_cache_instance = MagicMock()
            mock_cache_instance.last_threshold = 50
            mock_alert_cache.return_value = mock_cache_instance

            mock_get_btc_data.return_value = {"price": 95000, "ath": 100000}

            def stop_loop(_):
                raise SystemExit

            mock_sleep.side_effect = stop_loop

            with self.assertRaises(SystemExit):
                main.main()

        mock_get_btc_data.assert_called_once()
        mock_send_email.assert_not_called()
        mock_cache_instance.reset_week.assert_called_once()


if __name__ == "__main__":
    unittest.main()

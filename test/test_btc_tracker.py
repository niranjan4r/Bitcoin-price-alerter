import unittest
from unittest.mock import patch, MagicMock

from src.btc_tracker import get_btc_data, get_percentage_difference_from_ath


class TestBtcTracker(unittest.TestCase):

    @patch("btc_tracker.requests.get")
    def test_get_btc_data_success(self, mock_get):
        """Test fetching BTC data from mocked API."""
        mock_response_data = {
            "market_data": {
                "current_price": {"usd": 65000},
                "ath": {"usd": 69000}
            }
        }

        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_get.return_value = mock_response

        result = get_btc_data()

        mock_get.assert_called_once_with("https://api.coingecko.com/api/v3/coins/bitcoin")
        self.assertEqual(result["price"], 65000)
        self.assertEqual(result["ath"], 69000)
        self.assertIsInstance(result, dict)

    def test_get_percentage_difference_from_ath(self):
        """Test percentage difference calculation between price and ATH."""
        price = 50000
        ath = 100000

        result = get_percentage_difference_from_ath(price, ath)
        self.assertAlmostEqual(result, 100.0, places=2)

    def test_get_percentage_difference_from_ath_small_drop(self):
        """Test small drop calculation."""
        price = 95000
        ath = 100000

        result = get_percentage_difference_from_ath(price, ath)
        self.assertAlmostEqual(result, 5.26, places=2)


if __name__ == "__main__":
    unittest.main()

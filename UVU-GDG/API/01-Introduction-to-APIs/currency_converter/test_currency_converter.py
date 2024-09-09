import unittest
from currency_converter import get_real_time_rate, api_key

class TestCurrencyConverter(unittest.TestCase):

    def test_real_time_rate(self):
        rates = get_real_time_rate(api_key, "USD", ["EUR", "GBP"])
        self.assertIsNotNone(rates)
        self.assertIn("EUR", rates)
        self.assertIn("GBP", rates)

if __name__ == '__main__':
    unittest.main()
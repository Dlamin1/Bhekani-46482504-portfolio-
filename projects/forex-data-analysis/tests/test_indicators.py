import unittest
from analyze import Candle, sma, rsi, atr, analyse

class IndicatorTests(unittest.TestCase):
    def setUp(self):
        self.candles = [Candle(str(i), p, p+1, p-1, p) for i, p in enumerate([10,11,12,11,13,14,15,14,16,17,18,19,20,19,21,22])]

    def test_sma(self):
        self.assertEqual(sma([1,2,3,4], 3), 3)
        self.assertIsNone(sma([1,2], 3))

    def test_rsi_bounds(self):
        value = rsi([1,2,3,4,5,6], 3)
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, 100)

    def test_atr_positive(self):
        self.assertGreater(atr(self.candles, 3), 0)

    def test_analysis_has_observation(self):
        self.assertIn("observation", analyse(self.candles, 3, 5, 3))

if __name__ == "__main__": unittest.main()

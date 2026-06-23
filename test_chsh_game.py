import math
import unittest

from chsh_game import classical_always_zero, quantum_optimal, simulate, won_round


class ChshGameTest(unittest.TestCase):
    def test_winning_condition(self):
        self.assertTrue(won_round(0, 0, 0, 0))
        self.assertTrue(won_round(0, 1, 1, 1))
        self.assertTrue(won_round(1, 0, 0, 0))
        self.assertTrue(won_round(1, 1, 0, 1))
        self.assertFalse(won_round(1, 1, 0, 0))

    def test_classical_strategy_is_near_75_percent(self):
        result = simulate("classica", classical_always_zero, rounds=20_000, seed=1)
        self.assertAlmostEqual(result.win_rate, 0.75, delta=0.02)

    def test_quantum_strategy_is_near_theoretical_limit(self):
        expected = math.cos(math.pi / 8) ** 2
        result = simulate("quantica", quantum_optimal, rounds=20_000, seed=1)
        self.assertAlmostEqual(result.win_rate, expected, delta=0.02)


if __name__ == "__main__":
    unittest.main()

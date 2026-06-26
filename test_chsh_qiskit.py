import math
import unittest

from chsh_qiskit import build_circuit, won_round


def win_rate_for_input(x: int, y: int, shots: int, seed: int) -> float:
    """Roda o circuito de uma entrada e retorna a fracao de vitorias."""

    from qiskit_aer import AerSimulator

    simulator = AerSimulator(seed_simulator=seed)
    counts = simulator.run(build_circuit(x, y), shots=shots).result().get_counts()

    wins = 0
    for bitstring, freq in counts.items():
        b = int(bitstring[0])
        a = int(bitstring[1])
        if won_round(x, y, a, b):
            wins += freq
    return wins / shots


class ChshQiskitTest(unittest.TestCase):
    def test_winning_condition(self):
        self.assertTrue(won_round(0, 0, 1, 1))
        self.assertTrue(won_round(1, 1, 0, 1))
        self.assertFalse(won_round(1, 1, 1, 1))

    def test_each_input_is_near_theoretical_limit(self):
        expected = math.cos(math.pi / 8) ** 2  # ~= 0.8536
        for x in range(2):
            for y in range(2):
                rate = win_rate_for_input(x, y, shots=20_000, seed=7)
                self.assertAlmostEqual(rate, expected, delta=0.02)


if __name__ == "__main__":
    unittest.main()

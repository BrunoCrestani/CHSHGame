"""Simulador simples do jogo CHSH.

O objetivo e comparar uma estrategia classica com uma estrategia quantica
otima, sem depender de bibliotecas externas de computacao quantica.
"""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from typing import Callable


Bit = int
Strategy = Callable[[Bit, Bit, random.Random], tuple[Bit, Bit]]


@dataclass(frozen=True)
class SimulationResult:
    name: str
    rounds: int
    wins: int
    input_counts: dict[tuple[Bit, Bit], int]
    input_wins: dict[tuple[Bit, Bit], int]

    @property
    def win_rate(self) -> float:
        return self.wins / self.rounds


def won_round(x: Bit, y: Bit, a: Bit, b: Bit) -> bool:
    """Retorna True se a rodada satisfaz a condicao do jogo CHSH."""

    return (a ^ b) == (x & y)


def classical_always_zero(x: Bit, y: Bit, rng: random.Random) -> tuple[Bit, Bit]:
    """Estrategia classica simples: Alice e Bob sempre respondem 0."""

    return 0, 0


def quantum_optimal(x: Bit, y: Bit, rng: random.Random) -> tuple[Bit, Bit]:
    """Simula a correlacao quantica otima para o jogo CHSH.

    Alice mede em 0 ou pi/4. Bob mede em pi/8 ou -pi/8. Para o estado
    emaranhado |Phi+>, os resultados sao iguais com probabilidade
    cos^2(theta_a - theta_b). Essa escolha vence com probabilidade
    cos^2(pi/8), aproximadamente 85.36%.
    """

    alice_angles = {
        0: 0.0,
        1: math.pi / 4,
    }
    bob_angles = {
        0: math.pi / 8,
        1: -math.pi / 8,
    }

    delta = alice_angles[x] - bob_angles[y]
    probability_same = math.cos(delta) ** 2

    same_result = rng.random() < probability_same
    a = rng.randint(0, 1)
    b = a if same_result else a ^ 1
    return a, b


def simulate(
    name: str,
    strategy: Strategy,
    rounds: int,
    seed: int | None,
    verbose: bool = False,
) -> SimulationResult:
    rng = random.Random(seed)
    wins = 0
    input_counts = {(x, y): 0 for x in range(2) for y in range(2)}
    input_wins = {(x, y): 0 for x in range(2) for y in range(2)}
    progress_step = max(1, rounds // 4)

    if verbose:
        print(f"[log] Iniciando estrategia: {name}")

    for round_number in range(1, rounds + 1):
        x = rng.randint(0, 1)
        y = rng.randint(0, 1)
        a, b = strategy(x, y, rng)
        win = won_round(x, y, a, b)

        input_counts[(x, y)] += 1
        if win:
            wins += 1
            input_wins[(x, y)] += 1

        if verbose and round_number <= 8:
            status = "venceu" if win else "perdeu"
            print(
                "[log] "
                f"rodada {round_number:>2}: "
                f"x={x}, y={y}, a={a}, b={b}, "
                f"a XOR b={a ^ b}, x AND y={x & y} -> {status}"
            )

        if verbose and round_number % progress_step == 0:
            print(
                "[log] "
                f"{name}: {round_number}/{rounds} rodadas, "
                f"taxa parcial={wins / round_number * 100:.2f}%"
            )

    if verbose:
        print(f"[log] Finalizando estrategia: {name}")

    return SimulationResult(
        name=name,
        rounds=rounds,
        wins=wins,
        input_counts=input_counts,
        input_wins=input_wins,
    )


def format_result(result: SimulationResult, theoretical_rate: float) -> str:
    observed = result.win_rate * 100
    expected = theoretical_rate * 100
    return (
        f"{result.name:<24} "
        f"vitorias: {result.wins:>6}/{result.rounds:<6} "
        f"observado: {observed:>6.2f}% "
        f"teorico: {expected:>6.2f}%"
    )


def format_input_breakdown(result: SimulationResult) -> list[str]:
    lines = []

    for x in range(2):
        for y in range(2):
            total = result.input_counts[(x, y)]
            wins = result.input_wins[(x, y)]
            rate = wins / total * 100 if total else 0.0
            lines.append(f"  x={x}, y={y}: {wins:>5}/{total:<5} ({rate:>6.2f}%)")

    return lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simula o jogo CHSH.")
    parser.add_argument(
        "-n",
        "--rounds",
        type=int,
        default=10_000,
        help="numero de rodadas por estrategia (padrao: 10000)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="semente para resultados reproduziveis (padrao: 42)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="mostra logs de progresso e exemplos das primeiras rodadas",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.rounds <= 0:
        raise SystemExit("O numero de rodadas precisa ser positivo.")

    print("Jogo CHSH")
    print("Condicao de vitoria: a XOR b = x AND y")
    print(f"Rodadas por estrategia: {args.rounds}")
    print(f"Semente aleatoria: {args.seed}")
    print()

    classical = simulate(
        name="Classica: sempre 0",
        strategy=classical_always_zero,
        rounds=args.rounds,
        seed=args.seed,
        verbose=args.verbose,
    )
    quantum = simulate(
        name="Quantica: otima",
        strategy=quantum_optimal,
        rounds=args.rounds,
        seed=args.seed,
        verbose=args.verbose,
    )

    print(format_result(classical, theoretical_rate=0.75))
    print("Detalhe por entrada:")
    print("\n".join(format_input_breakdown(classical)))
    print()
    print(format_result(quantum, theoretical_rate=math.cos(math.pi / 8) ** 2))
    print("Detalhe por entrada:")
    print("\n".join(format_input_breakdown(quantum)))


if __name__ == "__main__":
    main()

"""Jogo CHSH usando um circuito quantico real no Qiskit."""

from __future__ import annotations

import argparse
import math

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


# Angulos otimos de medicao (em radianos), no plano X-Z da esfera de Bloch.
# Com estes angulos o estado de Bell vence o jogo com probabilidade cos^2(pi/8).
ALICE_ANGLES = {0: 0.0, 1: math.pi / 2}
BOB_ANGLES = {0: math.pi / 4, 1: -math.pi / 4}

THEORETICAL_QUANTUM_RATE = math.cos(math.pi / 8) ** 2  # ~= 0.8536


def build_circuit(x: int, y: int) -> QuantumCircuit:
    """Monta o circuito CHSH para uma escolha de bits (x, y).

    Qubit 0 -> Alice, qubit 1 -> Bob.
    """

    qc = QuantumCircuit(2, 2)

    # 1) Estado de Bell |Phi+>.
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    # 2) Cada jogador gira seu qubit para medir na base escolhida.
    qc.ry(-ALICE_ANGLES[x], 0)
    qc.ry(-BOB_ANGLES[y], 1)

    # 3) Medicao: bit 0 = resposta de Alice (a), bit 1 = resposta de Bob (b).
    qc.measure(0, 0)
    qc.measure(1, 1)
    return qc


def won_round(x: int, y: int, a: int, b: int) -> bool:
    """Condicao de vitoria do jogo CHSH."""

    return (a ^ b) == (x & y)


def run(rounds: int, seed: int | None, show_circuit: bool) -> None:
    # As quatro perguntas (x, y) sao igualmente provaveis, entao dividimos
    # o numero de rodadas igualmente entre elas.
    shots_per_input = max(1, rounds // 4)
    total_rounds = shots_per_input * 4

    if show_circuit:
        print("Exemplo de circuito (x=1, y=1):")
        print(build_circuit(1, 1).draw(output="text"))
        print()

    total_wins = 0
    print("Detalhe por entrada:")
    for x in range(2):
        for y in range(2):
            # Semente diferente por entrada para que as amostragens variem
            # de forma natural (e nao deem contagens identicas).
            input_seed = None if seed is None else seed + 2 * x + y
            simulator = AerSimulator(seed_simulator=input_seed)
            circuit = build_circuit(x, y)
            result = simulator.run(circuit, shots=shots_per_input).result()
            counts = result.get_counts()

            wins = 0
            for bitstring, freq in counts.items():
                # Qiskit imprime os bits como "b a" (mais significativo a esquerda).
                b = int(bitstring[0])
                a = int(bitstring[1])
                if won_round(x, y, a, b):
                    wins += freq

            total_wins += wins
            rate = wins / shots_per_input * 100
            need = "a = b" if (x & y) == 0 else "a != b"
            print(
                f"  x={x}, y={y} ({need:>6}): "
                f"{wins:>6}/{shots_per_input:<6} ({rate:6.2f}%)"
            )

    observed = total_wins / total_rounds * 100
    print()
    print(
        f"Taxa de vitoria quantica: {observed:.2f}%  "
        f"(teorico: {THEORETICAL_QUANTUM_RATE * 100:.2f}%)"
    )
    print("Limite classico: 75.00%")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Jogo CHSH com circuito quantico real (Qiskit + Aer)."
    )
    parser.add_argument(
        "-n",
        "--rounds",
        type=int,
        default=10_000,
        help="numero total de rodadas (padrao: 10000)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="semente do simulador para reproducibilidade (padrao: 42)",
    )
    parser.add_argument(
        "--show-circuit",
        action="store_true",
        help="mostra um exemplo do circuito quantico",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.rounds <= 0:
        raise SystemExit("O numero de rodadas precisa ser positivo.")

    print("Jogo CHSH")
    print("Condicao de vitoria: a XOR b = x AND y")
    print(f"Rodadas: {args.rounds} | semente: {args.seed}")
    print()
    run(args.rounds, args.seed, args.show_circuit)


if __name__ == "__main__":
    main()

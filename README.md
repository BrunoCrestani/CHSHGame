# Jogo CHSH

Este projeto demonstra o jogo CHSH usando um circuito quantico real no
Qiskit. Ele mostra a diferenca entre o limite classico (no maximo `75%` de
vitorias) e a estrategia quantica com emaranhamento (`~85.36%`).

## Ideia do jogo

Alice e Bob recebem bits aleatorios:

- Alice recebe `x`.
- Bob recebe `y`.
- Alice responde `a`.
- Bob responde `b`.

Eles vencem a rodada quando:

```text
a XOR b = x AND y
```

Alice e Bob nao podem se comunicar depois de receber `x` e `y`.

## Estrategia quantica

Antes do jogo, Alice e Bob compartilham um par emaranhado (estado de Bell):

```text
|Phi+> = (|00> + |11>) / sqrt(2)
```

Cada um mede o seu qubit em uma base que depende do bit recebido. Com os
angulos de medicao otimos, eles vencem com probabilidade:

```text
P(vitoria quantica) = cos^2(pi / 8) ~= 0.8536
```

O circuito e montado de verdade (`H` + `CNOT` para o emaranhamento, `Ry` para
as bases de medicao) e executado no simulador local Aer.

## Instalacao

Recomendado usar um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Como executar

```bash
python3 chsh_qiskit.py                 # 10000 rodadas
python3 chsh_qiskit.py --rounds 100000 # mais rodadas
python3 chsh_qiskit.py --show-circuit  # mostra o circuito
```

Exemplo de saida:

```text
Detalhe por entrada:
  x=0, y=0 ( a = b):   2103/2500   ( 84.12%)
  x=0, y=1 ( a = b):   2147/2500   ( 85.88%)
  x=1, y=0 ( a = b):   2097/2500   ( 83.88%)
  x=1, y=1 (a != b):   2171/2500   ( 86.84%)

Taxa de vitoria quantica: 85.18%  (teorico: 85.36%)
Limite classico: 75.00%
```

Como a simulacao usa medicoes aleatorias, os valores observados podem variar
um pouco a cada execucao.

## Testes

```bash
python3 -m unittest test_chsh_qiskit
```

## Arquivos

- `chsh_qiskit.py`: jogo com circuito quantico real (Qiskit + Aer).
- `test_chsh_qiskit.py`: testes automaticos.
- `requirements.txt`: dependencias.
- `slides/`: apresentacao em Beamer (LaTeX).

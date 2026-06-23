# Jogo CHSH

Este projeto simula o jogo CHSH, um exemplo classico usado para mostrar a
diferenca entre estrategias classicas e estrategias quanticas com
emaranhamento.

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

## Estrategias implementadas

- Estrategia classica: Alice e Bob sempre respondem `0`. Ela vence em torno de
  `75%` das rodadas.
- Estrategia quantica: simula as correlacoes de um par emaranhado com angulos
  de medicao otimos. Ela vence em torno de `85.36%` das rodadas.

O codigo nao usa uma biblioteca quantica pesada. Ele simula diretamente as
probabilidades teoricas:

```text
P(vitoria quantica) = cos^2(pi / 8) ~= 0.8536
```

## Como executar

```bash
python3 chsh_game.py
```

Tambem e possivel escolher o numero de rodadas:

```bash
python3 chsh_game.py --rounds 100000
```

Para ver logs de progresso e exemplos das primeiras rodadas:

```bash
python3 chsh_game.py --rounds 20 --verbose
```

Exemplo de saida:

```text
Jogo CHSH
Condicao de vitoria: a XOR b = x AND y
Rodadas por estrategia: 10000
Semente aleatoria: 42

Classica: sempre 0      vitorias:   7500/10000  observado:  75.00% teorico:  75.00%
Detalhe por entrada:
  x=0, y=0:  2500/2500  (100.00%)
  x=0, y=1:  2500/2500  (100.00%)
  x=1, y=0:  2500/2500  (100.00%)
  x=1, y=1:     0/2500  (  0.00%)

Quantica: otima         vitorias:   8536/10000  observado:  85.36% teorico:  85.36%
Detalhe por entrada:
  x=0, y=0:  2134/2500  ( 85.36%)
  x=0, y=1:  2134/2500  ( 85.36%)
  x=1, y=0:  2134/2500  ( 85.36%)
  x=1, y=1:  2134/2500  ( 85.36%)
```

Como a simulacao usa sorteio aleatorio, os valores observados podem variar um
pouco.

## Testes

```bash
python3 -m unittest
```

## Arquivos

- `chsh_game.py`: simulador principal.
- `test_chsh_game.py`: testes automaticos simples.

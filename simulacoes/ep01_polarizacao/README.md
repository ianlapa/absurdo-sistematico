# Episódio 1 — Por que pessoas razoáveis se polarizam?

## O modelo

Modelo de **confiança limitada** de Hegselmann & Krause (2002):

1. 100 pessoas, cada uma com uma opinião entre 0 e 1, sorteada ao acaso.
2. A cada rodada, cada pessoa só leva a sério quem pensa parecido com ela: quem está a até **ε** (épsilon, a "tolerância") de distância.
3. Ela passa a adotar a média das opiniões de quem escuta, incluindo a dela.

Ninguém mente, ninguém é teimoso, não tem algoritmo. Só muda o ε.

## Resultados do vídeo

Mesmas pessoas, mesmas opiniões iniciais (`seed = 42`), 10 rodadas:

| Tolerância (ε) | Resultado |
| --- | --- |
| 0,05 | 8 bolhas |
| 0,15 | 3 bolhas |
| 0,30 | consenso |

```bash
python modelo.py            # reproduz a tabela
python modelo.py 0.1 0.2    # experimente outras tolerâncias
```

Troque a `seed` em `simular()` e o número de bolhas muda um pouco: o padrão (pouca tolerância → muitas bolhas, muita tolerância → consenso) se mantém.

## Clipes

`python gerar_clipes.py` gera tudo em `saida/`:

| Arquivo | O que mostra |
| --- | --- |
| `01_abertura.mp4` | Título com o logo |
| `02_gancho_tres_cenarios.mp4` | Os três cenários rodando juntos |
| `03_regra_uma_pessoa.mp4` | Uma pessoa, a sua janela de tolerância e a média |
| `04_codigo.png` | A regra inteira em poucas linhas |
| `05_cenario_005.mp4`, `06_cenario_015.mp4`, `07_cenario_030.mp4` | Cada cenário sozinho |
| `08_comparacao_final.png` | Os três resultados lado a lado |
| `09_encerramento.mp4` | Frase final com o logo |
| `10_explicacoes_comuns.mp4`, `11_testemunho.mp4`, `12_confianca_limitada.mp4` | Os textos do bloco sobre epistemologia social |

## Para ler mais

- Hegselmann, R. & Krause, U. (2002). "Opinion Dynamics and Bounded Confidence: Models, Analysis and Simulation". *Journal of Artificial Societies and Social Simulation*, 5(3).
- O'Connor, C. & Weatherall, J. O. (2019). *The Misinformation Age: How False Beliefs Spread*. Yale University Press.
- Zollman, K. (2007). "The Communication Structure of Epistemic Communities". *Philosophy of Science*, 74(5).

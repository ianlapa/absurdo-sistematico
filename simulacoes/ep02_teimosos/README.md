# Episódio 2 — E se tiver gente que nunca muda de ideia?

## O modelo

O mesmo modelo do episódio 1, com um grupo de **teimosos**: pessoas paradas na opinião 1,0 que falam, mas não escutam ninguém. Quem estiver a até ε de distância delas as escuta, como escuta qualquer outra pessoa. Todo o resto segue a regra de antes: escuta quem está perto e vai para a média.

Uma pessoa conta como **capturada** quando termina com opinião ≥ 0,99, colada nos teimosos.

## Resultados do vídeo

Sociedade de 100 pessoas, `seed = 3`, 40 rodadas:

| Sociedade | Teimosos | Resultado |
| --- | --- | --- |
| Tolerante (ε = 0,40) | 0 | consenso em 0,51 |
| Tolerante (ε = 0,40) | 10 | consenso sobe para 0,57; ninguém capturado |
| Tolerante (ε = 0,40) | 20 | 100% capturados |
| Intolerante (ε = 0,05) | 20 | 6% capturados |
| Tolerância média (ε = 0,20) | 20 | 61% capturados |
| Tolerância média (ε = 0,20) | 50 | 17% capturados |

**O degrau** (ε = 0,40, média de 100 sociedades sorteadas): até 10 teimosos, nenhuma sociedade cai; com 12, 43%; com 20, 94%; a partir de 22, praticamente todas.

**Mais radicais, menos radicalização:** com 50 teimosos, quem está perto deles é puxado tão rápido que se afasta do resto e a ponte se rompe. Com 20, a puxada é lenta e arrasta mais gente. Hegselmann já tinha mostrado que, em certas regiões do modelo, mais radicais podem significar menos radicalização.

```bash
python modelo.py              # reproduz a tabela (rápido)
python modelo.py --completo   # também o degrau (alguns minutos)
```

## Clipes

`python gerar_clipes.py` gera tudo em `saida/` (o degrau e o mapa fazem milhares de simulações e levam alguns minutos):

| Arquivo | O que mostra |
| --- | --- |
| `e2_01_abertura.mp4` | Título do episódio com o logo |
| `e2_02_recap.mp4` | Sociedade tolerante chegando ao consenso |
| `e2_03_teimosos_10.mp4` | Com 10 teimosos: o consenso sobe |
| `e2_04_teimosos_20.mp4` | Com 20 teimosos: todo mundo é capturado |
| `e2_05_salto.png` | % capturada por número de teimosos: o degrau |
| `e2_06_intolerante.mp4` | Sociedade intolerante com 20 teimosos |
| `e2_07_20_vs_50.mp4` | 20 contra 50 teimosos, lado a lado |
| `e2_08_mapa.png` | Mapa da captura: tolerância × número de teimosos |
| `e2_09_encerramento.mp4` | Frase final com o logo |

## Para ler mais

- Hegselmann, R. & Krause, U. (2015). "Opinion Dynamics under the Influence of Radical Groups, Charismatic Leaders, and Other Constant Signals: A Simple Unifying Model". *Networks and Heterogeneous Media*, 10(3), 477–509.
- Popper, K. (1945). *A sociedade aberta e seus inimigos*, vol. 1 (nota sobre o paradoxo da tolerância).

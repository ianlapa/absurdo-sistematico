"""
Episódio 2 — E se tiver gente que nunca muda de ideia?

O modelo do episódio 1 (Hegselmann & Krause), com um grupo de "teimosos":
pessoas paradas no extremo (opinião 1,0) que falam, mas não escutam ninguém.
As outras seguem a mesma regra de antes: escutam quem está a até `epsilon`
de distância (teimosos incluídos) e adotam a média.

Extensão inspirada em Hegselmann & Krause (2015), "Opinion Dynamics under the
Influence of Radical Groups, Charismatic Leaders, and Other Constant Signals".

Uso:
    python modelo.py             # os resultados citados no vídeo
    python modelo.py --completo  # também o degrau (100 sociedades por ponto); leva alguns minutos
"""
import sys

import numpy as np


def simular(epsilon, n_teimosos, rodadas=40, n=100, seed=3, posicao=1.0):
    """Histórico das opiniões das n pessoas comuns: matriz (rodadas + 1) x n."""
    x = np.random.default_rng(seed).uniform(0, 1, n)
    teimosos = np.full(n_teimosos, posicao)            # nunca mudam
    historico = [x.copy()]
    for _ in range(rodadas):
        todos = np.concatenate([x, teimosos])
        escuta = np.abs(x[:, None] - todos[None, :]) <= epsilon
        x = (escuta * todos[None, :]).sum(1) / escuta.sum(1)
        historico.append(x.copy())
    return np.array(historico)


def fracao_capturada(historico, limiar=0.99):
    """Fração das pessoas comuns que terminam colada nos teimosos."""
    return (historico[-1] >= limiar).mean()


def fracao_media(epsilon, n_teimosos, sociedades=100, rodadas=40):
    """Média da fração capturada em várias sociedades sorteadas (seeds 0, 1, 2...)."""
    return np.mean([fracao_capturada(simular(epsilon, n_teimosos, rodadas, seed=s))
                    for s in range(sociedades)])


def pct(v):
    return f"{round(v * 100)}%"


if __name__ == "__main__":
    h0, h10, h20 = (simular(0.40, k) for k in (0, 10, 20))
    print("Sociedade tolerante (ε = 0,40)")
    print(f"  sem teimosos   → consenso em {h0[-1].mean():.2f}".replace(".", ","))
    print(f"  10 teimosos    → consenso em {h10[-1].mean():.2f}".replace(".", ",") + f", {pct(fracao_capturada(h10))} capturados")
    print(f"  20 teimosos    → {pct(fracao_capturada(h20))} capturados")
    print("Sociedade intolerante (ε = 0,05)")
    print(f"  20 teimosos    → {pct(fracao_capturada(simular(0.05, 20)))} capturados")
    print("Tolerância média (ε = 0,20)")
    for k in (20, 50):
        print(f"  {k} teimosos    → {pct(fracao_capturada(simular(0.20, k)))} capturados")
    if "--completo" in sys.argv:
        print("Degrau (ε = 0,40, média de 100 sociedades)")
        for k in range(0, 31, 2):
            print(f"  {k:2d} teimosos → {pct(fracao_media(0.40, k))}")

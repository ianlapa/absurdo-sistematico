"""
Episódio 1 — Por que pessoas razoáveis se polarizam?

Modelo de Hegselmann & Krause (2002), "confiança limitada":
- cada pessoa tem uma opinião entre 0 e 1;
- a cada rodada, ela só escuta quem está a até `epsilon` de distância dela;
- e passa a adotar a média das opiniões de quem escuta (incluindo a dela).

Uso:
    python modelo.py            # roda os três cenários do vídeo
    python modelo.py 0.2        # roda com outra tolerância
"""
import sys

import numpy as np


def simular(epsilon, n=100, rodadas=10, seed=42):
    """Devolve o histórico de opiniões: matriz (rodadas + 1) x n."""
    x = np.random.default_rng(seed).uniform(0, 1, n)  # opiniões iniciais ao acaso
    historico = [x.copy()]
    for _ in range(rodadas):
        distancia = np.abs(x[:, None] - x[None, :])    # distância entre todos os pares
        escuta = distancia <= epsilon                  # quem cada um leva a sério
        x = (escuta * x[None, :]).sum(1) / escuta.sum(1)
        historico.append(x.copy())
    return np.array(historico)


def contar_grupos(historico, casas=3):
    """Quantas opiniões diferentes sobraram no fim (cada uma é uma 'bolha')."""
    return len(np.unique(np.round(historico[-1], casas)))


if __name__ == "__main__":
    tolerancias = [float(a) for a in sys.argv[1:]] or [0.05, 0.15, 0.30]
    for eps in tolerancias:
        h = simular(eps)
        g = contar_grupos(h)
        resultado = "consenso" if g == 1 else f"{g} bolhas"
        print(f"ε = {eps:.2f} → {resultado}".replace(".", ","))

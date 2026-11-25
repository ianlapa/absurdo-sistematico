"""
Gera os clipes do episódio 2 (1920x1080, 30 fps) na pasta saida/.

Uso:
    python gerar_clipes.py                    # todos (o degrau e o mapa levam alguns minutos)
    python gerar_clipes.py abertura lado_a_lado   # só alguns (nomes na lista CLIPES no fim do arquivo)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator

from comum.estilo import (BG, FG, MUTED, GRID, VERDE, TERRACOTA, PALETA, FPS, marca, logo, ease, ramp,
                          num, nova_fig, salvar_video, salvar_imagem)
from modelo import simular as _simular, fracao_capturada, fracao_media

SAIDA = Path(__file__).resolve().parent / "saida"
N, SEED = 100, 3


def simular(eps, n_teimosos, rodadas, seed=SEED):
    return _simular(eps, n_teimosos, rodadas=rodadas, n=N, seed=seed)


INICIAL = np.random.default_rng(SEED).uniform(0, 1, N)
CORES = PALETA(INICIAL)

capturados = fracao_capturada

def preparar(ax, rodadas, fonte=16, ylabel=True):
    ax.set_facecolor(BG); ax.set_xlim(-0.3, rodadas + 0.3); ax.set_ylim(-0.04, 1.08)
    for s in ax.spines.values(): s.set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=fonte)
    ax.set_xlabel("rodadas de conversa", color=MUTED, fontsize=fonte + 2)
    if ylabel: ax.set_ylabel("opinião", color=MUTED, fontsize=fonte + 2)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    lc = LineCollection([], colors=CORES, linewidths=1.8, alpha=0.75); ax.add_collection(lc)
    cab = ax.scatter([], [], s=30, zorder=3)
    return lc, cab

def linha_teimosos(ax, n, rodadas, fonte=18):
    if n == 0: return None
    ax.plot([0, rodadas], [1.0, 1.0], color=TERRACOTA, lw=6, solid_capstyle="round", zorder=4)
    return ax.text(0.2, 1.035, f"{n} teimosos (nunca saem do 1)", color=TERRACOTA, fontsize=fonte,
                   fontweight="bold", va="bottom")

def desenhar(lc, cab, h, r, rodadas):
    k, frac = int(np.floor(r)), r - np.floor(r)
    if k >= rodadas:
        xs, ys = np.arange(rodadas + 1), h
    else:
        xs = np.append(np.arange(k + 1), r)
        ys = np.vstack([h[:k + 1], h[k] + (h[k + 1] - h[k]) * frac])
    lc.set_segments([np.column_stack([xs, ys[:, j]]) for j in range(N)])
    cab.set_offsets(np.column_stack([np.full(N, xs[-1]), ys[-1]])); cab.set_color(CORES)

# ---------- e2_01 abertura ----------
def abertura():
    fig = nova_fig()
    c = logo(fig, [0.36, 0.64, 0.28, 0.28])
    ep = fig.text(0.5, 0.56, "EPISÓDIO 2", ha="center", color=VERDE, fontsize=26, fontweight="bold")
    t = fig.text(0.5, 0.36, "E se tiver gente que\nnunca muda de ideia?", ha="center", va="center",
                 color=FG, fontsize=64, fontweight="bold", linespacing=1.3)
    def f(i):
        s = i / FPS; c.set_alpha(ramp(s, 0.2)); ep.set_alpha(ramp(s, 0.5)); t.set_alpha(ramp(s, 0.8, 0.8))
    salvar_video(fig, f, 4.5, SAIDA / "e2_01_abertura.mp4")

# ---------- cenário de um painel ----------
def cenario(eps, n, rodadas, titulo, resultado, nome, dur_sim=7.0):
    h = simular(eps, n, rodadas)
    fig = nova_fig(); marca(fig)
    ax = fig.add_axes([0.10, 0.17, 0.80, 0.62])
    lc, cab = preparar(ax, rodadas); linha_teimosos(ax, n, rodadas)
    fig.text(0.5, 0.88, titulo, ha="center", color=FG, fontsize=38, fontweight="bold")
    rod = fig.text(0.96, 0.95, "", ha="right", color=MUTED, fontsize=22)
    res = fig.text(0.5, 0.045, resultado, ha="center", color=FG, fontsize=40, fontweight="bold")
    dur = 0.8 + dur_sim + 4.5
    def f(i):
        s = i / FPS; r = ease((s - 0.8) / dur_sim) * rodadas
        desenhar(lc, cab, h, r, rodadas); rod.set_text(f"rodada {int(round(r))}")
        res.set_alpha(ramp(s, 0.8 + dur_sim + 0.3, 0.8))
    salvar_video(fig, f, dur, SAIDA / nome)
    return h

# ---------- e2_07: 20 vs 50 ----------
def lado_a_lado():
    rodadas, eps = 30, 0.20
    hs = [simular(eps, 20, rodadas), simular(eps, 50, rodadas)]
    finais = [capturados(simular(eps, n, 40)) for n in (20, 50)]  # mesma conta do roteiro (40 rodadas)
    fig = nova_fig(); marca(fig)
    fig.text(0.5, 0.89, "Tolerância média · ε = 0,20", ha="center", color=FG, fontsize=36, fontweight="bold")
    objs, ress = [], []
    for i, (h, n, cap) in enumerate(zip(hs, (20, 50), finais)):
        ax = fig.add_axes([0.07 + i * 0.47, 0.2, 0.42, 0.56])
        lc, cab = preparar(ax, rodadas, fonte=14, ylabel=(i == 0)); linha_teimosos(ax, n, rodadas, fonte=16)
        objs.append((lc, cab, h))
        ress.append(fig.text(0.28 + i * 0.47, 0.055, f"{n} teimosos → {round(cap * 100)}% capturados",
                             ha="center", color=FG if i == 0 else VERDE, fontsize=32, fontweight="bold"))
    dur_sim = 9.0
    def f(i):
        s = i / FPS; r = ease((s - 0.8) / dur_sim) * rodadas
        for lc, cab, h in objs: desenhar(lc, cab, h, r, rodadas)
        for k, t in enumerate(ress): t.set_alpha(ramp(s, 10.2 + 1.2 * k, 0.8))
    salvar_video(fig, f, 15.0, SAIDA / "e2_07_20_vs_50.mp4")

# ---------- gráficos agregados ----------
def salto():
    ns = list(range(0, 31, 2))
    ys = [fracao_media(0.40, n) * 100 for n in ns]  # 100 sociedades por ponto
    fig = nova_fig(); marca(fig)
    ax = fig.add_axes([0.12, 0.17, 0.80, 0.60]); ax.set_facecolor(BG)
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]: ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=18)
    ax.plot(ns, ys, color=TERRACOTA, lw=5, marker="o", ms=12, zorder=3)
    ax.set_ylim(-4, 104); ax.set_xlim(-1, 31)
    ax.set_xlabel("número de teimosos (para cada 100 pessoas)", color=MUTED, fontsize=20)
    ax.set_ylabel("% da sociedade capturada", color=MUTED, fontsize=20)
    ax.grid(axis="y", color=GRID, lw=1)
    ax.axvspan(10, 20, color=VERDE, alpha=0.12)
    ax.annotate("até 10: ninguém cai", (10, ys[5]), xytext=(1, 30), color=FG, fontsize=22, fontweight="bold")
    ax.annotate("com 20: 94%", (20, ys[10]), xytext=(21.5, 80), color=FG, fontsize=22, fontweight="bold")
    fig.text(0.5, 0.87, "Não é uma rampa. É um degrau.", ha="center", color=FG, fontsize=40, fontweight="bold")
    fig.text(0.5, 0.05, "sociedade tolerante (ε = 0,40) · média de 100 sociedades por ponto",
             ha="center", color=MUTED, fontsize=18)
    salvar_imagem(fig, SAIDA / "e2_05_salto.png")

def mapa():
    epss = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
    ns = [0, 5, 10, 15, 20, 30, 40, 50]
    M = np.array([[fracao_media(e, n, sociedades=40) * 100 for n in ns] for e in epss])
    cmap = LinearSegmentedColormap.from_list("perigo", [BG, "#C9A77F", TERRACOTA, "#41362F"])
    fig = nova_fig(); marca(fig)
    ax = fig.add_axes([0.2, 0.13, 0.6, 0.66])
    ax.imshow(M, cmap=cmap, vmin=0, vmax=100, origin="lower", aspect="auto")
    for i in range(len(epss)):
        for j in range(len(ns)):
            v = M[i, j]
            ax.text(j, i, f"{v:.0f}%", ha="center", va="center", fontsize=17, fontweight="bold",
                    color=BG if v > 55 else FG)
    ax.set_xticks(range(len(ns)), [str(n) for n in ns]); ax.set_yticks(range(len(epss)), [num(e) for e in epss])
    ax.tick_params(colors=MUTED, labelsize=18, length=0)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xlabel("número de teimosos", color=MUTED, fontsize=20)
    ax.set_ylabel("tolerância (ε)", color=MUTED, fontsize=20)
    fig.text(0.5, 0.88, "Onde os teimosos vencem", ha="center", color=FG, fontsize=42, fontweight="bold")
    fig.text(0.5, 0.035, "% da sociedade capturada · média de 40 sociedades por célula",
             ha="center", color=MUTED, fontsize=18)
    salvar_imagem(fig, SAIDA / "e2_08_mapa.png")

def encerramento():
    fig = nova_fig()
    t = fig.text(0.5, 0.58, "A tolerância que nos une\né a mesma porta por onde\nos teimosos entram.",
                 ha="center", va="center", color=FG, fontsize=54, fontweight="bold", linespacing=1.35)
    c = logo(fig, [0.40, 0.08, 0.20, 0.20])
    def f(i):
        s = i / FPS; t.set_alpha(ramp(s, 0.3, 0.8)); c.set_alpha(ramp(s, 2.0))
    salvar_video(fig, f, 6.0, SAIDA / "e2_09_encerramento.mp4")

def _recap():
    h0 = simular(0.40, 0, 10)
    cenario(0.40, 0, 10, "Sociedade tolerante · ε = 0,40", f"→ consenso em {num(h0[-1].mean())}",
            "e2_02_recap.mp4", dur_sim=5.0)


def _teimosos_10():
    h10 = simular(0.40, 10, 10)
    cenario(0.40, 10, 10, "Tolerante + 10 teimosos", f"→ consenso sobe para {num(h10[-1].mean())}",
            "e2_03_teimosos_10.mp4", dur_sim=6.0)


def _teimosos_20():
    h20 = simular(0.40, 20, 30)
    cenario(0.40, 20, 30, "Tolerante + 20 teimosos", f"→ {round(capturados(h20) * 100)}% capturados",
            "e2_04_teimosos_20.mp4", dur_sim=10.0)


def _intolerante():
    hi = simular(0.05, 20, 10)
    cenario(0.05, 20, 10, "Intolerante (ε = 0,05) + 20 teimosos", f"→ só {round(capturados(hi) * 100)}% capturados",
            "e2_06_intolerante.mp4", dur_sim=6.0)


CLIPES = {
    "abertura": abertura,
    "recap": _recap,
    "teimosos_10": _teimosos_10,
    "teimosos_20": _teimosos_20,
    "salto": salto,
    "intolerante": _intolerante,
    "lado_a_lado": lado_a_lado,
    "mapa": mapa,
    "encerramento": encerramento,
}

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(CLIPES)
    for nome in pedidos:
        if nome not in CLIPES:
            sys.exit(f"clipe desconhecido: {nome}. Opções: {', '.join(CLIPES)}")
        CLIPES[nome]()

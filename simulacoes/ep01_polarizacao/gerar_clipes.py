"""
Gera os clipes do episódio 1 (1920x1080, 30 fps) na pasta saida/.

Uso:
    python gerar_clipes.py                 # todos os clipes
    python gerar_clipes.py regra codigo    # só alguns (nomes na lista CLIPES no fim do arquivo)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from comum.estilo import (BG, FG, MUTED, GRID, VERDE, PALETA, FPS, marca, logo, ease, ramp,
                          nova_fig, salvar_video, salvar_imagem)
from modelo import simular, contar_grupos

SAIDA = Path(__file__).resolve().parent / "saida"
N, RODADAS, SEED = 100, 10, 42

CENARIOS = [(0.05, "Pouca tolerância"), (0.15, "Tolerância média"), (0.30, "Muita tolerância")]
HIST = {e: simular(e, n=N, rodadas=RODADAS, seed=SEED) for e, _ in CENARIOS}
INICIAL = HIST[0.05][0]
CORES = PALETA(INICIAL)

n_grupos = contar_grupos
def rotulo_resultado(g): return "→ consenso" if g == 1 else f"→ {g} bolhas"

def preparar_painel(ax, fonte=13):
    ax.set_facecolor(BG); ax.set_xlim(-0.3, RODADAS + 0.3); ax.set_ylim(-0.04, 1.04)
    for s in ax.spines.values(): s.set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=fonte)
    ax.set_xlabel("rodadas de conversa", color=MUTED, fontsize=fonte + 2)
    lc = LineCollection([], colors=CORES, linewidths=1.8, alpha=0.75); ax.add_collection(lc)
    cab = ax.scatter([], [], s=30, zorder=3)
    return lc, cab

def desenhar_ate(lc, cab, h, r):
    k, frac = int(np.floor(r)), r - np.floor(r)
    if k >= RODADAS:
        xs, ys = np.arange(RODADAS + 1), h
    else:
        xs = np.append(np.arange(k + 1), r)
        ys = np.vstack([h[:k + 1], h[k] + (h[k + 1] - h[k]) * frac])
    lc.set_segments([np.column_stack([xs, ys[:, j]]) for j in range(N)])
    cab.set_offsets(np.column_stack([np.full(N, xs[-1]), ys[-1]])); cab.set_color(CORES)

# ---------- 01 abertura ----------
def abertura():
    fig = nova_fig()
    c = logo(fig, [0.36, 0.62, 0.28, 0.28])
    t = fig.text(0.5, 0.40, "Por que pessoas razoáveis\nse polarizam?", ha="center", va="center",
                 color=FG, fontsize=64, fontweight="bold", linespacing=1.3)
    def f(i):
        s = i / FPS; c.set_alpha(ramp(s, 0.2)); t.set_alpha(ramp(s, 0.6, 0.8))
    salvar_video(fig, f, 4.0, SAIDA / "01_abertura.mp4")

# ---------- 02 gancho ----------
def gancho():
    fig = nova_fig(); marca(fig)
    axes = [fig.add_axes([0.05 + i * 0.315, 0.12, 0.28, 0.76]) for i in range(3)]
    obj = [preparar_painel(ax) for ax in axes]
    def f(i):
        r = ease((i / FPS - 0.5) / 7.0) * RODADAS
        for (lc, cab), (e, _) in zip(obj, CENARIOS): desenhar_ate(lc, cab, HIST[e], r)
    salvar_video(fig, f, 10.0, SAIDA / "02_gancho_tres_cenarios.mp4")

# ---------- 03 regra de uma pessoa ----------
def regra():
    eps, alvo = 0.15, int(np.argmin(np.abs(INICIAL - 0.635)))
    x0 = INICIAL[alvo]
    jitter = np.random.default_rng(1).uniform(-1, 1, N)
    dentro = np.abs(INICIAL - x0) <= eps
    media = INICIAL[dentro].mean()
    fig = nova_fig(); marca(fig); ax = fig.add_axes([0.08, 0.25, 0.84, 0.5]); ax.set_facecolor(BG)
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-1.6, 1.6); ax.set_yticks([])
    for s in ["left", "right", "top"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID); ax.tick_params(colors=MUTED, labelsize=16)
    ax.set_xlabel("opinião", color=MUTED, fontsize=18)
    pts = ax.scatter(INICIAL, jitter, s=90, c=[CORES[j] for j in range(N)])
    eu = ax.scatter([x0], [0], s=420, facecolor="none", edgecolor=FG, linewidth=3, zorder=5)
    faixa = ax.axvspan(x0 - eps, x0 + eps, color=VERDE, alpha=0)
    lbl_eps = ax.text(x0, 1.45, "", ha="center", color=FG, fontsize=22)
    linha_media = ax.axvline(media, color=VERDE, lw=3, ls="--", alpha=0)
    lbl_media = ax.text(media, -1.5, "média de quem ela escuta", ha="center", color=VERDE, fontsize=20, fontweight="bold", alpha=0)
    topo = fig.text(0.5, 0.86, "", ha="center", color=FG, fontsize=34)
    rastro, = ax.plot([], [], color=FG, lw=3, zorder=4)
    falas = [(0.0, "100 pessoas, cada uma com uma opinião"), (2.5, "Olhe para esta pessoa"),
             (4.5, "Ela só escuta quem está até ε de distância"), (8.0, "e vai para a média dessas opiniões")]
    def f(i):
        s = i / FPS
        topo.set_text([txt for t0, txt in falas if s >= t0][-1])
        eu.set_alpha(ramp(s, 2.5))
        faixa.set_alpha(0.18 * ramp(s, 4.5))
        lbl_eps.set_text("← ε →   ← ε →" if s >= 4.5 else "")
        lbl_eps.set_alpha(ramp(s, 4.5))
        a_out = 1 - 0.85 * ramp(s, 6.0)
        alphas = np.where(dentro, 1.0, a_out) * ramp(s, 0.0)
        cores = [(*CORES[j][:3], alphas[j]) for j in range(N)]
        pts.set_color(cores)
        linha_media.set_alpha(ramp(s, 8.0)); lbl_media.set_alpha(ramp(s, 8.0))
        xn = x0 + (media - x0) * ease((s - 9.5) / 1.5)
        eu.set_offsets([[xn, 0]])
        rastro.set_data([x0, xn], [0, 0]); rastro.set_alpha(ramp(s, 9.5))
    salvar_video(fig, f, 13.0, SAIDA / "03_regra_uma_pessoa.mp4")

# ---------- 04 código ----------
def codigo():
    linhas = [
        ("# cada pessoa tem uma opinião entre 0 e 1", MUTED),
        ("x = np.random.uniform(0, 1, 100)", FG),
        ("", FG),
        ("for rodada in range(10):", FG),
        ("    # quem está a até ε de distância de quem?", MUTED),
        ("    escuta = abs(x[:, None] - x[None, :]) <= epsilon", FG),
        ("    # cada um adota a média de quem escuta", MUTED),
        ("    x = (escuta * x).sum(1) / escuta.sum(1)", FG),
    ]
    fig = nova_fig(); marca(fig)
    fig.text(0.5, 0.86, "O modelo inteiro", ha="center", color=FG, fontsize=40, fontweight="bold")
    for k, (txt, cor) in enumerate(linhas):
        fig.text(0.14, 0.70 - k * 0.07, txt, color=cor, fontsize=30, family="DejaVu Sans Mono")
    fig.text(0.5, 0.08, "Hegselmann & Krause (2002)", ha="center", color=MUTED, fontsize=20)
    salvar_imagem(fig, SAIDA / "04_codigo.png")

# ---------- 05-07 cenários ----------
def cenario(eps, rotulo, nome):
    h = HIST[eps]; g = n_grupos(h)
    fig = nova_fig(); marca(fig); ax = fig.add_axes([0.10, 0.17, 0.80, 0.62])
    lc, cab = preparar_painel(ax, fonte=16); ax.set_ylabel("opinião", color=MUTED, fontsize=18)
    fig.text(0.5, 0.88, f"{rotulo}   ·   ε = {eps:.2f}".replace(".", ","), ha="center", color=FG, fontsize=40, fontweight="bold")
    rod = fig.text(0.96, 0.95, "", ha="right", color=MUTED, fontsize=22)
    res = fig.text(0.5, 0.045, rotulo_resultado(g), ha="center", color=FG, fontsize=42, fontweight="bold")
    def f(i):
        s = i / FPS; r = ease((s - 0.8) / 7.0) * RODADAS
        desenhar_ate(lc, cab, h, r); rod.set_text(f"rodada {int(round(r))}")
        res.set_alpha(ramp(s, 8.5, 0.8))
    salvar_video(fig, f, 13.0, SAIDA / nome)

# ---------- 08 comparação ----------
def comparacao():
    fig = nova_fig(); marca(fig)
    fig.text(0.5, 0.89, "Mesmas pessoas, mesmas opiniões iniciais. Só muda a tolerância.",
             ha="center", color=FG, fontsize=30)
    for i, (e, rot) in enumerate(CENARIOS):
        ax = fig.add_axes([0.06 + i * 0.31, 0.21, 0.27, 0.52])
        lc, cab = preparar_painel(ax); desenhar_ate(lc, cab, HIST[e], RODADAS)
        ax.set_title(f"{rot}\nε = {e:.2f}".replace(".", ","), color=FG, fontsize=22, pad=16, linespacing=1.4)
        ax.text(0.5, -0.27, rotulo_resultado(n_grupos(HIST[e])), transform=ax.transAxes,
                ha="center", color=FG, fontsize=30, fontweight="bold")
    salvar_imagem(fig, SAIDA / "08_comparacao_final.png")

# ---------- 09 encerramento ----------
def encerramento():
    fig = nova_fig()
    t = fig.text(0.5, 0.58, "Ninguém aqui é irracional,\nsó muda quem escuta quem.", ha="center", va="center",
                 color=FG, fontsize=58, fontweight="bold", linespacing=1.4)
    c = logo(fig, [0.40, 0.10, 0.20, 0.20])
    def f(i):
        s = i / FPS; t.set_alpha(ramp(s, 0.3, 0.8)); c.set_alpha(ramp(s, 2.0))
    salvar_video(fig, f, 6.0, SAIDA / "09_encerramento.mp4")

# ---------- 10-12 bloco 2 ----------
def explicacoes():
    fig = nova_fig(); marca(fig)
    palavras = ["irracionalidade?", "má-fé?", "manipulação?"]
    txts = [fig.text(0.2 + 0.3 * k, 0.60, w, ha="center", color=FG, fontsize=46, fontweight="bold")
            for k, w in enumerate(palavras)]
    ou = fig.text(0.307, 0.36, "ou a ", ha="right", color=FG, fontsize=58, fontweight="bold")
    est = fig.text(0.307, 0.36, "estrutura da conversa?", ha="left", color=VERDE, fontsize=58, fontweight="bold")
    def f(i):
        s = i / FPS
        for k, t in enumerate(txts):
            t.set_alpha(ramp(s, 0.5 + 1.5 * k) * (1 - 0.75 * ramp(s, 6.5)))
        a = ramp(s, 7.0, 0.8); ou.set_alpha(a); est.set_alpha(a)
    salvar_video(fig, f, 12.0, SAIDA / "10_explicacoes_comuns.mp4")

def testemunho():
    fig = nova_fig(); marca(fig)
    rot = fig.text(0.5, 0.70, "EPISTEMOLOGIA SOCIAL", ha="center", color=VERDE, fontsize=26, fontweight="bold")
    t1 = fig.text(0.5, 0.52, "Quase tudo o que a gente sabe,", ha="center", color=FG, fontsize=54, fontweight="bold")
    t2 = fig.text(0.5, 0.40, "a gente sabe porque alguém contou.", ha="center", color=FG, fontsize=54, fontweight="bold")
    def f(i):
        s = i / FPS; rot.set_alpha(ramp(s, 0.3)); t1.set_alpha(ramp(s, 1.0, 0.8)); t2.set_alpha(ramp(s, 2.5, 0.8))
    salvar_video(fig, f, 9.0, SAIDA / "11_testemunho.mp4")

def confianca():
    fig = nova_fig(); marca(fig)
    tit = fig.text(0.5, 0.74, "confiança limitada", ha="center", color=FG, fontsize=64, fontweight="bold")
    sub = fig.text(0.5, 0.65, "dar menos peso a quem pensa muito diferente de nós", ha="center", color=MUTED, fontsize=28)
    ax = fig.add_axes([0.15, 0.18, 0.70, 0.36]); ax.set_xlim(0, 1); ax.set_ylim(-1, 1); ax.axis("off")
    xs = np.linspace(0.03, 0.97, 17); centro = 0.5
    pts = ax.scatter(xs, np.zeros_like(xs), s=420, c=[PALETA(x) for x in xs])
    eu = ax.scatter([centro], [0], s=1200, facecolor="none", edgecolor=FG, linewidth=3)
    faixa = ax.axvspan(centro - 0.2, centro + 0.2, color=VERDE, alpha=0)
    def f(i):
        s = i / FPS
        tit.set_alpha(ramp(s, 0.3, 0.8)); sub.set_alpha(ramp(s, 1.5))
        eu.set_alpha(ramp(s, 3.0)); faixa.set_alpha(0.18 * ramp(s, 4.0))
        dentro = np.abs(xs - centro) <= 0.2
        alphas = np.where(dentro, 1.0, 1 - 0.8 * ramp(s, 5.0)) * ramp(s, 2.2)
        pts.set_color([(*PALETA(x)[:3], a) for x, a in zip(xs, alphas)])
    salvar_video(fig, f, 10.0, SAIDA / "12_confianca_limitada.mp4")

CLIPES = {
    "abertura": abertura,
    "gancho": gancho,
    "regra": regra,
    "codigo": codigo,
    "cenario_005": lambda: cenario(0.05, "Pouca tolerância", "05_cenario_005.mp4"),
    "cenario_015": lambda: cenario(0.15, "Tolerância média", "06_cenario_015.mp4"),
    "cenario_030": lambda: cenario(0.30, "Muita tolerância", "07_cenario_030.mp4"),
    "comparacao": comparacao,
    "encerramento": encerramento,
    "explicacoes": explicacoes,
    "testemunho": testemunho,
    "confianca": confianca,
}

if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(CLIPES)
    for nome in pedidos:
        if nome not in CLIPES:
            sys.exit(f"clipe desconhecido: {nome}. Opções: {', '.join(CLIPES)}")
        CLIPES[nome]()

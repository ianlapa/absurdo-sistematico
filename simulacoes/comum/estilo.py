"""
Identidade visual e utilitários de animação compartilhados pelos episódios.

Tudo sai em 1920x1080, 30 fps. Os vídeos são gravados com o ffmpeg.
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.colors import LinearSegmentedColormap

RAIZ = Path(__file__).resolve().parent.parent
PASTA_MARCA = RAIZ / "marca"

FPS = 30

# ---------- cores ----------
BG = "#D6D1C3"         # bege (fundo)
FG = "#41362F"         # marrom escuro (texto)
MUTED = "#7D7468"      # texto secundário
GRID = "#BDB5A4"       # eixos e grades
VERDE = "#5F7065"      # verde-sálvia (destaque)
MARROM = "#4A3F36"
TERRACOTA = "#8A4F38"  # destaque quente (teimosos, alertas)

# cor de cada agente pela opinião inicial: verde (0) -> ocre -> terracota (1)
PALETA = LinearSegmentedColormap.from_list("absurdo", ["#4E6155", "#9A7647", "#7E412C"])

plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]


def _carregar(nome):
    caminho = PASTA_MARCA / nome
    return plt.imread(caminho) if caminho.exists() else None


LOGO = _carregar("logo_transparente.png")
FIGURA = _carregar("figura.png")


# ---------- elementos de marca ----------
def marca(fig):
    """Símbolo discreto no canto superior esquerdo (se o arquivo existir)."""
    if FIGURA is None:
        return
    ax = fig.add_axes([0.02, 0.88, 0.07, 0.10])
    ax.imshow(FIGURA, alpha=0.55)
    ax.axis("off")


def logo(fig, caixa, alpha=1.0):
    """Logo numa caixa [x, y, largura, altura] em fração da figura. Devolve o objeto para animar."""
    ax = fig.add_axes(caixa)
    ax.axis("off")
    if LOGO is None:
        return ax.text(0.5, 0.5, "ABSURDO SISTEMÁTICO", ha="center", va="center",
                       color=FG, fontsize=28, fontweight="bold", alpha=alpha)
    return ax.imshow(LOGO, alpha=alpha)


# ---------- animação ----------
def ease(u):
    """Suaviza o movimento (começa e termina devagar)."""
    u = np.clip(u, 0, 1)
    return u * u * (3 - 2 * u)


def ramp(t, inicio, dur=0.6):
    """0 antes de `inicio`, sobe até 1 em `dur` segundos. Usado para fade-in."""
    return float(np.clip((t - inicio) / dur, 0, 1))


def num(v, casas=2):
    """Número com vírgula decimal: 0.51 -> '0,51'."""
    return f"{v:.{casas}f}".replace(".", ",")


def nova_fig():
    return plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=BG)


def salvar_video(fig, quadro, duracao, caminho):
    """Renderiza `quadro(i)` para cada quadro e grava um mp4."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    anim = FuncAnimation(fig, quadro, frames=int(duracao * FPS))
    anim.save(caminho, writer=FFMpegWriter(fps=FPS, bitrate=6000,
              extra_args=["-pix_fmt", "yuv420p", "-preset", "veryfast"]),
              savefig_kwargs={"facecolor": BG})
    plt.close(fig)
    print("ok", caminho.name)


def salvar_imagem(fig, caminho):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho, facecolor=BG)
    plt.close(fig)
    print("ok", caminho.name)

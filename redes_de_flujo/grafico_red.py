"""
Genera dos gráficos de la red de flujo para el problema de backup de antenas:
  1. grafico_red.png       — red original con capacidades
  2. grafico_residual.png  — red residual después de Edmonds-Karp

Usa el caso1.toml: n=5, k=2, b=3, D=7.

Requiere: pip install matplotlib networkx
"""

import copy
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

sys.path.insert(0, str(Path(__file__).parent))
from antenas import _construir_red
from algoritmos import _edmonds_karp

# ── Parámetros (caso1) ──────────────────────────────────────────────────────
D = 7
k = 2
b = 3

distancias = [
    [0, 5, 6, 7, 8],
    [5, 0, 1, 2, 3],
    [3, 1, 0, 1, 2],
    [7, 2, 1, 0, 1],
    [8, 6, 2, 1, 0],
]
n = len(distancias)

# ── Construcción de la red ───────────────────────────────────────────────────
cap_orig, S_idx, T_idx = _construir_red(distancias, k, b, D)
cap_residual = copy.deepcopy(cap_orig)
_edmonds_karp(cap_residual, S_idx, T_idx)

# ── Etiquetas de nodos (índice numérico → nombre legible) ───────────────────
def label(v):
    if v == S_idx: return "S"
    if v == T_idx: return "T"
    if 1 <= v <= n: return f"A{v}"
    return f"B{v - n}"

total = T_idx + 1

# ── Posición en capas ────────────────────────────────────────────────────────
def build_pos():
    pos = {}
    pos[label(S_idx)] = (0, (n - 1) / 2)
    for i in range(1, n + 1):
        pos[label(i)] = (1, n - 1 - (i - 1))
    for j in range(1, n + 1):
        pos[label(n + j)] = (2, n - 1 - (j - 1))
    pos[label(T_idx)] = (3, (n - 1) / 2)
    return pos

pos = build_pos()


# ════════════════════════════════════════════════════════════════════════════
# Plot 1 — Red original
# ════════════════════════════════════════════════════════════════════════════
def plot_original():
    G = nx.DiGraph()
    edge_labels = {}

    for u in range(total):
        for v in range(total):
            c = cap_orig[u][v]
            if c > 0:
                lu, lv = label(u), label(v)
                color = ("steelblue" if u == S_idx else
                         "tomato"    if v == T_idx else "dimgray")
                G.add_edge(lu, lv, color=color)
                edge_labels[(lu, lv)] = f"cap={c}"

    _, ax = plt.subplots(figsize=(11, 6))

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=1100,
                           node_color=[
                               "steelblue" if n_ == "S" else
                               "tomato"    if n_ == "T" else
                               "lightsteelblue" if n_.startswith("A") else
                               "lightsalmon"
                               for n_ in G.nodes()
                           ])
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight="bold")
    edge_colors = [G[u][v]["color"] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors,
                           arrows=True, arrowsize=18,
                           connectionstyle="arc3,rad=0.08", width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 ax=ax, font_size=7, label_pos=0.35)

    leyenda = [
        mpatches.Patch(color="steelblue", label=f"S → Aᵢ  (cap = k = {k})"),
        mpatches.Patch(color="dimgray",   label="Aᵢ → Bⱼ  (cap = 1, si d[i][j] < D)"),
        mpatches.Patch(color="tomato",    label=f"Bⱼ → T  (cap = b = {b})"),
    ]
    ax.legend(handles=leyenda, loc="lower center",
              bbox_to_anchor=(0.5, -0.13), ncol=3, fontsize=9)

    for x, etq in [(0, "Fuente"), (1, "Antenas\n(piden backup)"),
                   (2, "Antenas\n(dan backup)"), (3, "Sumidero")]:
        ax.text(x, n + 0.1, etq, ha="center", va="bottom",
                fontsize=9, color="dimgray", style="italic")

    ax.set_title(f"Red de flujo original — n={n}, k={k}, b={b}, D={D}", fontsize=13)
    ax.axis("off")
    plt.tight_layout()
    salida = Path(__file__).parent / "grafico_red.png"
    plt.savefig(salida, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Guardado: {salida}")


# ════════════════════════════════════════════════════════════════════════════
# Plot 2 — Red residual
# ════════════════════════════════════════════════════════════════════════════
def plot_residual():
    G = nx.DiGraph()
    edge_labels = {}

    for u in range(total):
        for v in range(total):
            orig = cap_orig[u][v]
            res  = cap_residual[u][v]

            if orig == 0 and res == 0:
                continue  # arista inexistente

            lu, lv = label(u), label(v)

            if orig > 0 and res == 0:
                # arista saturada: el flujo usó toda la capacidad
                G.add_edge(lu, lv, color="lightgray", style="solid")
                edge_labels[(lu, lv)] = "0"

            elif orig > 0 and res > 0:
                # arista con capacidad restante
                color = ("steelblue" if u == S_idx else
                         "tomato"    if v == T_idx else "dimgray")
                G.add_edge(lu, lv, color=color, style="solid")
                edge_labels[(lu, lv)] = str(res)

            elif orig == 0 and res > 0:
                # arista inversa: creada por el flujo
                G.add_edge(lu, lv, color="seagreen", style="dashed")
                edge_labels[(lu, lv)] = str(res)

    _, ax = plt.subplots(figsize=(11, 6))

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=1100,
                           node_color=[
                               "steelblue" if n_ == "S" else
                               "tomato"    if n_ == "T" else
                               "lightsteelblue" if n_.startswith("A") else
                               "lightsalmon"
                               for n_ in G.nodes()
                           ])
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight="bold")

    # dibujar aristas separando sólidas y punteadas
    solid  = [(u, v) for u, v in G.edges() if G[u][v]["style"] == "solid"]
    dashed = [(u, v) for u, v in G.edges() if G[u][v]["style"] == "dashed"]
    solid_colors  = [G[u][v]["color"] for u, v in solid]
    dashed_colors = [G[u][v]["color"] for u, v in dashed]

    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=solid,
                           edge_color=solid_colors,
                           arrows=True, arrowsize=18,
                           connectionstyle="arc3,rad=0.08", width=2)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=dashed,
                           edge_color=dashed_colors,
                           arrows=True, arrowsize=18,
                           connectionstyle="arc3,rad=0.08", width=1.5,
                           style="dashed")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 ax=ax, font_size=7, label_pos=0.35)

    leyenda = [
        mpatches.Patch(color="steelblue", label=f"S → Aᵢ  cap restante"),
        mpatches.Patch(color="dimgray",   label=f"Aᵢ → Bⱼ  cap restante"),
        mpatches.Patch(color="tomato",    label=f"Bⱼ → T  cap restante"),
        mpatches.Patch(color="lightgray", label="Arista saturada (cap = 0)"),
        mpatches.Patch(color="seagreen",  label="Arista inversa (punteada)"),
    ]
    ax.legend(handles=leyenda, loc="lower center",
              bbox_to_anchor=(0.5, -0.15), ncol=5, fontsize=8)

    for x, etq in [(0, "Fuente"), (1, "Antenas\n(piden backup)"),
                   (2, "Antenas\n(dan backup)"), (3, "Sumidero")]:
        ax.text(x, n + 0.1, etq, ha="center", va="bottom",
                fontsize=9, color="dimgray", style="italic")

    ax.set_title(f"Red residual tras Edmonds-Karp — n={n}, k={k}, b={b}, D={D}", fontsize=13)
    ax.axis("off")
    plt.tight_layout()
    salida = Path(__file__).parent / "grafico_residual.png"
    plt.savefig(salida, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Guardado: {salida}")


# ════════════════════════════════════════════════════════════════════════════
# Plot 3 — Aristas usadas en la reconstrucción
# ════════════════════════════════════════════════════════════════════════════
def plot_solucion():
    """
    Muestra la red original coloreando las aristas que forman la solución:
      - A_i → B_j saturadas (flujo = 1): gold / naranja — asignaciones elegidas
      - A_i → B_j no usadas:             lightgray      — descartadas
      - S → A_i y B_j → T:               igual que la red original
    """
    G = nx.DiGraph()
    edge_labels = {}

    for u in range(total):
        for v in range(total):
            c = cap_orig[u][v]
            if c == 0:
                continue

            lu, lv = label(u), label(v)
            res = cap_residual[u][v]
            flujo = c - res  # flujo que circuló por esta arista

            if u == S_idx:
                # S → A_i: resaltar con el flujo que salió
                G.add_edge(lu, lv, color="steelblue", width=2.0)
                edge_labels[(lu, lv)] = f"{flujo}/{c}"
            elif v == T_idx:
                # B_j → T: mostrar flujo recibido
                G.add_edge(lu, lv, color="tomato", width=2.0)
                edge_labels[(lu, lv)] = f"{flujo}/{c}"
            else:
                # A_i → B_j: dorado si fue elegida, gris si no
                if flujo == 1:
                    G.add_edge(lu, lv, color="goldenrod", width=2.5)
                    edge_labels[(lu, lv)] = "1"
                else:
                    G.add_edge(lu, lv, color="lightgray", width=1.0)

    _, ax = plt.subplots(figsize=(11, 6))

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=1100,
                           node_color=[
                               "steelblue" if n_ == "S" else
                               "tomato"    if n_ == "T" else
                               "lightsteelblue" if n_.startswith("A") else
                               "lightsalmon"
                               for n_ in G.nodes()
                           ])
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight="bold")

    widths      = [G[u][v]["width"] for u, v in G.edges()]
    edge_colors = [G[u][v]["color"] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, ax=ax,
                           edge_color=edge_colors, width=widths,
                           arrows=True, arrowsize=18,
                           connectionstyle="arc3,rad=0.08")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 ax=ax, font_size=7, label_pos=0.35)

    leyenda = [
        mpatches.Patch(color="steelblue",  label=f"S → Aᵢ"),
        mpatches.Patch(color="goldenrod",  label="Aᵢ → Bⱼ  elegida (flujo = 1)"),
        mpatches.Patch(color="lightgray",  label="Aᵢ → Bⱼ  descartada"),
        mpatches.Patch(color="tomato",     label=f"Bⱼ → T"),
    ]
    ax.legend(handles=leyenda, loc="lower center",
              bbox_to_anchor=(0.5, -0.13), ncol=4, fontsize=9)

    for x, etq in [(0, "Fuente"), (1, "Antenas\n(piden backup)"),
                   (2, "Antenas\n(dan backup)"), (3, "Sumidero")]:
        ax.text(x, n + 0.1, etq, ha="center", va="bottom",
                fontsize=9, color="dimgray", style="italic")

    ax.set_title(
        f"Solución reconstruida — n={n}, k={k}, b={b}, D={D}\n"
        f"Etiquetas: flujo/capacidad",
        fontsize=12,
    )
    ax.axis("off")
    plt.tight_layout()
    salida = Path(__file__).parent / "grafico_solucion.png"
    plt.savefig(salida, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Guardado: {salida}")


# ── Main ─────────────────────────────────────────────────────────────────────
plot_original()
plot_residual()
plot_solucion()

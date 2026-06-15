"""
Genera un gráfico de la red de flujo para el problema de backup de antenas.
Usa el ejemplo de 3 antenas del informe: k=1, b=2, D=10.

Requiere: pip install matplotlib networkx
"""

import matplotlib
matplotlib.use("Agg")  # sin ventana, guarda directo a archivo
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# ── Parámetros del ejemplo ──────────────────────────────────────────────────
distancias = [
    [0,  8, 16],
    [8,  0,  8],
    [16, 8,  0],
]
n = 3
k = 1
b = 2
D = 10

# ── Construir el grafo dirigido ─────────────────────────────────────────────
G = nx.DiGraph()

S = "S"
T = "T"
izq = [f"A{i}" for i in range(1, n + 1)]   # nodos izquierdos (piden backup)
der = [f"B{j}" for j in range(1, n + 1)]   # nodos derechos  (dan backup)

G.add_node(S)
G.add_node(T)
G.add_nodes_from(izq)
G.add_nodes_from(der)

# S → A_i  (capacidad k)
for ai in izq:
    G.add_edge(S, ai, cap=k, color="steelblue")

# A_i → B_j  (capacidad 1, si d[i][j] < D y i≠j)
for i in range(n):
    for j in range(n):
        if i != j and distancias[i][j] < D:
            G.add_edge(izq[i], der[j], cap=1, color="gray")

# B_j → T  (capacidad b)
for bj in der:
    G.add_edge(bj, T, cap=b, color="tomato")

# ── Layout manual en capas ──────────────────────────────────────────────────
pos = {}
pos[S] = (0, 1)
for idx, ai in enumerate(izq):
    pos[ai] = (1, idx)
for idx, bj in enumerate(der):
    pos[bj] = (2, idx)
pos[T] = (3, 1)

# ── Colores de aristas ──────────────────────────────────────────────────────
edge_colors  = [G[u][v]["color"] for u, v in G.edges()]
edge_labels  = {(u, v): f"cap={G[u][v]['cap']}" for u, v in G.edges()}

# ── Dibujo ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))

node_colors = []
for node in G.nodes():
    if node == S:
        node_colors.append("steelblue")
    elif node == T:
        node_colors.append("tomato")
    elif node.startswith("A"):
        node_colors.append("lightsteelblue")
    else:
        node_colors.append("lightsalmon")

nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                       node_size=1200)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=11, font_weight="bold")
nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors,
                       arrows=True, arrowsize=20,
                       connectionstyle="arc3,rad=0.08",
                       width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                             ax=ax, font_size=8, label_pos=0.35)

# ── Leyenda ─────────────────────────────────────────────────────────────────
leyenda = [
    mpatches.Patch(color="steelblue",     label=f"S → Aᵢ  (cap = k = {k})"),
    mpatches.Patch(color="gray",          label="Aᵢ → Bⱼ  (cap = 1, si d[i][j] < D)"),
    mpatches.Patch(color="tomato",        label=f"Bⱼ → T  (cap = b = {b})"),
]
ax.legend(handles=leyenda, loc="lower center",
          bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=9)

# ── Anotaciones de capa ─────────────────────────────────────────────────────
for x, etiqueta in [(0, "Fuente"), (1, "Antenas\n(piden backup)"),
                    (2, "Antenas\n(dan backup)"), (3, "Sumidero")]:
    ax.text(x, n - 0.2, etiqueta, ha="center", va="bottom",
            fontsize=9, color="dimgray", style="italic")

ax.set_title(f"Red de flujo — ejemplo n={n}, k={k}, b={b}, D={D}", fontsize=13)
ax.axis("off")
plt.tight_layout()

salida = "grafico_red.png"
plt.savefig(salida, dpi=150, bbox_inches="tight")
print(f"Gráfico guardado en: {salida}")

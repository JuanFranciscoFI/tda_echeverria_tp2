"""
Genera casos de prueba aleatorios para el problema de conjuntos de backup.

Las antenas se ubican en coordenadas 2D aleatorias dentro de un área cuadrada
y las distancias se calculan como distancia euclídea (redondeada a entero).

Uso:
    python generar_caso.py <n> <k> <b> <D> [nombre_salida]

Ejemplo:
    python generar_caso.py 20 3 4 50 casos/caso_grande.toml

Si se omite el nombre de salida, imprime el TOML por stdout.
"""

import math
import random
import sys
from pathlib import Path


def generar_distancias(n: int, area: int = 100, seed: int | None = None) -> list[list[int]]:
    """Genera una matriz de distancias euclídeas para n antenas en un área de area×area."""
    rng = random.Random(seed)
    coords = [(rng.uniform(0, area), rng.uniform(0, area)) for _ in range(n)]
    dist = []
    for i in range(n):
        fila = []
        for j in range(n):
            if i == j:
                fila.append(0)
            else:
                dx = coords[i][0] - coords[j][0]
                dy = coords[i][1] - coords[j][1]
                fila.append(round(math.sqrt(dx * dx + dy * dy), 2))
        dist.append(fila)
    return dist, coords


def _formatear_fila(fila: list) -> str:
    valores = ", ".join(str(v) for v in fila)
    return f"    [{valores}]"


def generar_toml(n: int, k: int, b: int, D: float, seed: int | None = None) -> str:
    distancias, coords = generar_distancias(n, seed=seed)

    vecinos_por_antena = [
        sum(1 for j in range(n) if j != i and distancias[i][j] < D)
        for i in range(n)
    ]
    min_vecinos = min(vecinos_por_antena)
    advertencia = ""
    if min_vecinos < k:
        advertencia = (
            f"# ADVERTENCIA: la antena con menos vecinos tiene {min_vecinos} (necesita k={k}).\n"
            f"# Probablemente no tenga solución. Aumentá D o reducí k.\n"
        )

    filas_toml = "\n".join(_formatear_fila(fila) for fila in distancias)
    coordenadas_comentario = "  ".join(f"A{i+1}=({x:.1f},{y:.1f})" for i, (x, y) in enumerate(coords))

    return (
        f"# Caso generado aleatoriamente  n={n}  k={k}  b={b}  D={D}  seed={seed}\n"
        f"# Coordenadas: {coordenadas_comentario}\n"
        f"{advertencia}"
        f"\n"
        f"D = {D}\n"
        f"k = {k}\n"
        f"b = {b}\n"
        f"\n"
        f"distancias = [\n{filas_toml},\n]\n"
    )


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)

    n   = int(sys.argv[1])
    k   = int(sys.argv[2])
    b   = int(sys.argv[3])
    D   = float(sys.argv[4])
    out = sys.argv[5] if len(sys.argv) > 5 else None
    seed = int(sys.argv[6]) if len(sys.argv) > 6 else 42

    contenido = generar_toml(n, k, b, D, seed=seed)

    if out:
        ruta = Path(__file__).parent / out
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(contenido, encoding="utf-8")
        print(f"Caso guardado en {ruta}")
    else:
        print(contenido)

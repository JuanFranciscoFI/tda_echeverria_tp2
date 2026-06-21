"""
Backup de antenas — algoritmo principal
=======================================

Encuentra el conjunto de backup de tamaño k para cada una de las n antenas,
de forma tal que ninguna antena aparezca en más de b conjuntos de backup,
o indica que no existe solución posible.

La solución se basa en flujo máximo (Edmonds-Karp). La red de flujo tiene la
siguiente estructura:

    S  →  A_i   capacidad k      (antena i necesita exactamente k backups)
    A_i → B_j   capacidad 1      (j puede ser backup de i, si d[i][j] < D)
    B_j → T     capacidad b      (j aparece en a lo sumo b conjuntos)

Existe solución ⟺ flujo máximo = n·k.
"""

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # pip install tomli  (Python < 3.11)

import logging
import sys
from pathlib import Path

from algoritmos import _edmonds_karp

logger = logging.getLogger("antenas")


# ─────────────────────────────────────────────────────────────────────────────
# Construcción de la red de flujo
# ─────────────────────────────────────────────────────────────────────────────

def _node_label(v, n, S, T):
    if v == S:
        return "S"
    if v == T:
        return "T"
    if 1 <= v <= n:
        return f"A{v}"
    return f"B{v - n}"


def _construir_red(distancias, k, b, D):
    """
    Devuelve (cap, S, T) donde cap es la matriz de capacidades de la red.

    Numeración de nodos:
        0        → fuente S
        1 .. n   → A_i  (antena i solicita backup)
        n+1..2n  → B_j  (antena j provee backup)
        2n+1     → sumidero T
    """
    n = len(distancias)
    S = 0
    T = 2 * n + 1
    total = T + 1

    cap = [[0] * total for _ in range(total)]

    logger.debug("--- Construcción de la red de flujo ---")
    for i in range(1, n + 1):
        cap[S][i] = k
        logger.debug("  S -> A%d  cap=%d", i, k)

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j and distancias[i - 1][j - 1] < D:
                cap[i][n + j] = 1
                logger.debug(
                    "  A%d -> B%d  cap=1  (d=%.4g < D=%.4g)",
                    i, j, distancias[i - 1][j - 1], D,
                )

    for j in range(1, n + 1):
        cap[n + j][T] = b
        logger.debug("  B%d -> T  cap=%d", j, b)

    return cap, S, T


# ─────────────────────────────────────────────────────────────────────────────
# Reconstrucción de los conjuntos desde la red residual
# ─────────────────────────────────────────────────────────────────────────────

def _reconstruir(cap, distancias, D, n):
    """
    Lee los conjuntos de backup a partir de las aristas saturadas A_i → B_j.
    Una arista A_i → B_j estaba en la red original con cap=1; si ahora vale 0,
    el flujo la atravesó, es decir, j ∈ backup(i).
    """
    conjuntos = []
    for i in range(1, n + 1):
        backup = [
            j
            for j in range(1, n + 1)
            if i != j and distancias[i - 1][j - 1] < D and cap[i][n + j] == 0
        ]
        conjuntos.append(backup)
    return conjuntos


# ─────────────────────────────────────────────────────────────────────────────
# Interfaz pública
# ─────────────────────────────────────────────────────────────────────────────

def obtener_conjunto_backup(distancias, k, b, D):
    """
    Parámetros
    ----------
    distancias : lista de listas nxn  —  distancias entre antenas (0-indexed)
    k          : int  —  tamaño requerido del conjunto de backup
    b          : int  —  máximo de conjuntos de backup en que puede aparecer una antena
    D          : float —  distancia máxima para ser vecino (exclusiva: d < D)

    Retorna
    -------
    lista de n listas con índices 1-based de las antenas de backup,
    o None si no existe solución.
    """
    n = len(distancias)
    cap, S, T = _construir_red(distancias, k, b, D)

    label_fn = lambda v: _node_label(v, n, S, T)
    logger.debug("--- Edmonds-Karp ---")
    flujo = _edmonds_karp(cap, S, T, logger=logger, label_fn=label_fn)
    logger.debug("Flujo maximo = %d  (objetivo n*k = %d)", flujo, n * k)

    if flujo != n * k:
        logger.debug("Flujo < n*k => sin solucion.")
        return None

    logger.debug("--- Reconstruccion de conjuntos ---")
    conjuntos = _reconstruir(cap, distancias, D, n)
    for i, backup in enumerate(conjuntos, start=1):
        logger.debug("  Antena %d: backup = %s", i, backup)
    return conjuntos


# ─────────────────────────────────────────────────────────────────────────────
# Lectura de archivos .toml
# ─────────────────────────────────────────────────────────────────────────────

def cargar_caso(ruta):
    """Lee un archivo .toml y devuelve (distancias, k, b, D)."""
    with open(ruta, "rb") as f:
        datos = tomllib.load(f)
    return datos["distancias"], datos["k"], datos["b"], datos["D"]


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def _uso():
    print(__doc__)
    sys.exit(0)


def _setup_logger(verbose: bool) -> None:
    if verbose:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        _uso()

    verbose = "--verbose" in args or "-v" in args
    args = [a for a in args if a not in ("--verbose", "-v")]
    _setup_logger(verbose)

    ruta = Path(__file__).parent / args[0]
    if not ruta.exists():
        print(f"Error: no se encontró el archivo '{ruta}'")
        sys.exit(1)

    distancias, k, b, D = cargar_caso(ruta)
    n = len(distancias)

    print(f"Caso : {ruta.name}")
    print(f"n={n}  k={k}  b={b}  D={D}")
    print()

    resultado = obtener_conjunto_backup(distancias, k, b, D)

    if resultado is None:
        print("No existe solución posible.")
        print(f"(el flujo máximo es menor a n·k = {n}·{k} = {n * k})")
    else:
        print("Solución encontrada:")
        for i, backup in enumerate(resultado, start=1):
            print(f"  Antena {i}: backup = {backup}")

        # Verificación rápida de apariciones
        from collections import Counter
        apariciones = Counter(j for backup in resultado for j in backup)
        print()
        print("Apariciones como backup:")
        for j in range(1, n + 1):
            veces = apariciones.get(j, 0)
            ok = "ok" if veces <= b else f"VIOLA b={b}"
            print(f"  Antena {j}: {veces} vez/veces  [{ok}]")


if __name__ == "__main__":
    main()

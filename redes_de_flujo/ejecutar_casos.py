"""
Ejecuta todos los casos de prueba y muestra una tabla con:
  - nombre del caso
  - parámetros (n, k, b, D)
  - resultado (solución / sin solución)
  - tiempo de ejecución en ms

Guarda el resultado en informe/resultados/flujo/resultados.txt

Uso:
    python ejecutar_casos.py
"""

import time
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from antenas import obtener_conjunto_backup

CASOS_DIR  = Path(__file__).parent / "casos"
SALIDA_DIR = Path(__file__).parent.parent / "informe" / "resultados" / "flujo"

CASOS = [
    "caso1.toml",
    "caso_b_igual_k.toml",
    "caso_b_menor_k.toml",
    "caso_d_chico.toml",
    "caso_d_amplio.toml",
    "caso_ajustado.toml",
    "caso_matching_perfecto.toml",
    "caso_mediano.toml",
    "caso_grande.toml",
    "caso_grande_imposible.toml",
]


def cargar(ruta):
    with open(ruta, "rb") as f:
        d = tomllib.load(f)
    return d["distancias"], d["k"], d["b"], d["D"]


def _construir_tabla():
    col_nombre = 28
    col_params = 20
    col_result = 16
    col_tiempo = 12

    sep    = "-" * (col_nombre + col_params + col_result + col_tiempo + 7)
    header = (
        f"{'Caso':<{col_nombre}} "
        f"{'Parametros':<{col_params}} "
        f"{'Resultado':<{col_result}} "
        f"{'Tiempo (ms)':>{col_tiempo}}"
    )

    lineas = [sep, header, sep]

    for nombre in CASOS:
        ruta = CASOS_DIR / nombre
        if not ruta.exists():
            lineas.append(f"{'[no encontrado]':<{col_nombre}} {nombre}")
            continue

        distancias, k, b, D = cargar(ruta)
        n = len(distancias)
        params = f"n={n} k={k} b={b} D={D}"

        t0 = time.perf_counter()
        resultado = obtener_conjunto_backup(distancias, k, b, D)
        t1 = time.perf_counter()

        ms = (t1 - t0) * 1000
        estado = "Solucion" if resultado is not None else "Sin solucion"
        nombre_sin_ext = nombre.replace(".toml", "")

        lineas.append(
            f"{nombre_sin_ext:<{col_nombre}} "
            f"{params:<{col_params}} "
            f"{estado:<{col_result}} "
            f"{ms:>{col_tiempo}.2f}"
        )

    lineas.append(sep)
    return lineas


def ejecutar_todos():
    lineas = _construir_tabla()

    # stdout
    print("\n".join(lineas))

    # archivo
    SALIDA_DIR.mkdir(parents=True, exist_ok=True)
    salida = SALIDA_DIR / "resultados.txt"
    salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"\nResultados guardados en: {salida}")


if __name__ == "__main__":
    ejecutar_todos()

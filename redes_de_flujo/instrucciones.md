# Instrucciones — backup de antenas

## antenas.py — algoritmo principal

Encuentra el conjunto de backup de tamaño k para cada una de las n antenas,
de forma tal que ninguna antena aparezca en más de b conjuntos de backup,
o indica que no existe solución posible.

La solución se basa en flujo máximo (Edmonds-Karp). La red de flujo tiene la
siguiente estructura:

```
S  →  A_i   capacidad k      (antena i necesita exactamente k backups)
A_i → B_j   capacidad 1      (j puede ser backup de i, si d[i][j] < D)
B_j → T     capacidad b      (j aparece en a lo sumo b conjuntos)
```

Existe solución ⟺ flujo máximo = n·k.

### Requerimientos

- **Python 3.10+**
- Lectura de archivos `.toml`:
  - **Python 3.11+**: usa `tomllib` incluido en la biblioteca estándar, sin instalación adicional.
  - **Python 3.10**: requiere instalar `tomli`:
    ```bash
    pip install tomli
    ```

El código detecta automáticamente cuál importar:
```python
try:
    import tomllib        # stdlib desde Python 3.11
except ModuleNotFoundError:
    import tomli as tomllib  # fallback para Python 3.10
```

### Uso desde la línea de comandos

```bash
# Ejecutar con un archivo de caso .toml
python antenas.py casos/caso1.toml

# Ver ayuda
python antenas.py --help
```

### Uso como módulo

```python
from antenas import obtener_conjunto_backup

distancias = [
    [0, 8, 16],
    [8, 0,  8],
    [16, 8,  0],
]
resultado = obtener_conjunto_backup(distancias, k=1, b=2, D=10)
# resultado → [[2], [1], [2]]  (índices 1-based)
# o None si no existe solución
```

---

## generar_caso.py — generador de casos de prueba

Genera archivos `.toml` con instancias aleatorias del problema de backup de antenas.
Las antenas se ubican en coordenadas 2D aleatorias dentro de un área de 100×100 y las
distancias se calculan como distancia euclídea redondeada a dos decimales.

### Uso

```
python generar_caso.py <n> <k> <b> <D> [archivo_salida] [seed]
```

| Argumento        | Tipo    | Descripción                                                           |
|------------------|---------|-----------------------------------------------------------------------|
| `n`              | entero  | Cantidad de antenas                                                   |
| `k`              | entero  | Tamaño del conjunto de backup de cada antena                          |
| `b`              | entero  | Máximo de conjuntos de backup en que puede aparecer cada antena       |
| `D`              | decimal | Distancia máxima para ser vecino (exclusiva: `d < D`)                 |
| `archivo_salida` | string  | Ruta del `.toml` a guardar (opcional; si se omite imprime por stdout) |
| `seed`           | entero  | Semilla para reproducibilidad (opcional; default `42`)                |

### Ejemplos

```bash
# Caso pequeño — imprime por stdout
python generar_caso.py 5 2 3 50

# Caso mediano — guarda en archivo
python generar_caso.py 20 3 4 40 casos/caso_mediano.toml

# Caso grande con semilla fija
python generar_caso.py 100 3 5 35 casos/caso_grande.toml 7

# Caso sin solución probable (D muy chico)
python generar_caso.py 10 3 2 10 casos/caso_imposible.toml
```

### Cómo elegir parámetros solucionables

Para que exista solución se necesitan cumplir dos condiciones:

1. **Vecinos suficientes**: cada antena debe tener al menos `k` vecinos con `d < D`.
   - Si el generador detecta que alguna antena tiene menos vecinos que `k`, imprime una advertencia en el `.toml`.
   - Aumentar `D` o reducir `k` amplía el margen.

2. **Capacidad global**: `b >= k` (con `b < k` nunca hay solución, independientemente de las distancias).

### Formato del archivo generado

```toml
# Caso generado aleatoriamente  n=5  k=2  b=3  D=50.0  seed=42
# Coordenadas: A1=(37.5,95.1)  A2=(73.2,5.9)  ...

D = 50.0
k = 2
b = 3

distancias = [
    [0, 43.2, 31.1, ...],
    ...
]
```

---

## ejecutar_casos.py — ejecución de todos los casos

Corre todos los casos de `casos/` y guarda la tabla de resultados en
`informe/resultados/flujo/resultados.txt`.

```bash
python ejecutar_casos.py
```

# Instrucciones — generador de casos de prueba

Genera archivos `.toml` con instancias aleatorias del problema de backup de antenas.
Las antenas se ubican en coordenadas 2D aleatorias dentro de un área de 100×100 y las
distancias se calculan como distancia euclídea redondeada a dos decimales.

## Uso

```
python generar_caso.py <n> <k> <b> <D> [archivo_salida] [seed]
```

| Argumento        | Tipo    | Descripción                                              |
|------------------|---------|----------------------------------------------------------|
| `n`              | entero  | Cantidad de antenas                                      |
| `k`              | entero  | Tamaño del conjunto de backup de cada antena             |
| `b`              | entero  | Máximo de conjuntos de backup en que puede aparecer cada antena |
| `D`              | decimal | Distancia máxima para ser vecino (exclusiva: `d < D`)    |
| `archivo_salida` | string  | Ruta del `.toml` a guardar (opcional; si se omite imprime por stdout) |
| `seed`           | entero  | Semilla para reproducibilidad (opcional; default `42`)   |

## Ejemplos

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

## Cómo elegir parámetros solucionables

Para que exista solución se necesitan cumplir dos condiciones:

1. **Vecinos suficientes**: cada antena debe tener al menos `k` vecinos con `d < D`.
   - Si el generador detecta que alguna antena tiene menos vecinos que `k`, imprime una advertencia en el `.toml`.
   - Aumentar `D` o reducir `k` amplía el margen.

2. **Capacidad global**: la suma de cuotas de backup debe cubrir la demanda total: `n·b >= n·k`, es decir, `b >= k`.
   - Con `b < k` nunca hay solución.

## Ejecutar la solución sobre el caso generado

```bash
python antenas.py casos/caso_mediano.toml
```

## Formato del archivo generado

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

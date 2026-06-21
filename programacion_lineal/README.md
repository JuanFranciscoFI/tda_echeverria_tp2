# Trabajo Práctico 2 - Teoría de Algoritmos

## Ejecución del programa

El programa fue desarrollado en Python y utiliza `PuLP` para modelar el problema de programación lineal.  
Para resolverlo se utiliza el solver `HiGHS`.

### 1. Crear entorno virtual

Desde la raíz del proyecto:

```bash
python3 -m venv .venv
```

o, según la instalación de Python:

```bash
python -m venv .venv
```

### 2. Activar entorno virtual

En Linux / macOS:

```bash
source .venv/bin/activate
```

En Windows:

```bash
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install pulp highspy
```

### 4. Ejecutar el programa

```bash
python3 code/programacion_lineal.py
```

o, según la instalación de Python:

```bash
python code/programacion_lineal.py
```

from grafo import Grafo

# 1. Camino simple
def generar_grafo_1():
    g = Grafo()

    for i in range(10):
        g.agregar_vertice(str(i))

    for i in range(9):
        g.agregar_arista(str(i), str(i + 1))

    return g


# 2. Ciclo impar
def generar_grafo_2():
    g = Grafo()

    for i in range(15):
        g.agregar_vertice(str(i))

    for i in range(15):
        g.agregar_arista(str(i), str((i + 1) % 15))

    return g


# 3. Bipartito completo K10,10
def generar_grafo_3():
    g = Grafo()

    for i in range(20):
        g.agregar_vertice(str(i))

    for i in range(10):
        for j in range(10, 20):
            g.agregar_arista(str(i), str(j))

    return g

# 4. Grilla 5x6
def generar_grafo_4():
    g = Grafo()

    filas = 5
    columnas = 6

    for i in range(filas):
        for j in range(columnas):
            g.agregar_vertice(f"{i}-{j}")

    for i in range(filas):
        for j in range(columnas):

            if i + 1 < filas:
                g.agregar_arista(f"{i}-{j}", f"{i+1}-{j}")

            if j + 1 < columnas:
                g.agregar_arista(f"{i}-{j}", f"{i}-{j+1}")

    return g


# 5. Grafo casi completo fijo
def generar_grafo_5():
    g = Grafo()

    n = 20

    for i in range(n):
        g.agregar_vertice(str(i))

    for i in range(n):
        for j in range(i + 1, n):
            if (i + j) % 5 != 0:
                g.agregar_arista(str(i), str(j))

    return g


# 6. Dos cliques unidos por puentes
def generar_grafo_6():
    g = Grafo()

    for i in range(30):
        g.agregar_vertice(str(i))

    # clique 1
    for i in range(15):
        for j in range(i + 1, 15):
            g.agregar_arista(str(i), str(j))

    # clique 2
    for i in range(15, 30):
        for j in range(i + 1, 30):
            g.agregar_arista(str(i), str(j))

    # puentes fijos
    puentes = [
        (0, 15),
        (1, 16),
        (2, 17),
        (3, 18),
        (4, 19),
        (5, 20),
        (6, 21),
        (7, 22),
        (8, 23),
        (9, 24)
    ]

    for a, b in puentes:
        g.agregar_arista(str(a), str(b))

    return g


def obtener_grafo(opcion) -> Grafo:
    if opcion == 1:
        return generar_grafo_1()

    if opcion == 2:
        return generar_grafo_2()

    if opcion == 3:
        return generar_grafo_3()

    if opcion == 4:
        return generar_grafo_4()

    if opcion == 5:
        return generar_grafo_5()

    if opcion == 6:
        return generar_grafo_6()

    return None
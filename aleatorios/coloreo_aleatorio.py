from grafo import Grafo
from generador_grafos import obtener_grafo
from metricas import obtener_metricas_coloreo

import random

REINTENTOS_MAXIMOS = 10

def color_aleatorio():
    return random.randint(1, 3)


def colorear_grafo(grafo: Grafo):
    vertices = grafo.obtener_vertices()

    vertices_coloreados = {}

    for vertice in vertices:
        vertices_coloreados[vertice] = color_aleatorio()

    return vertices_coloreados


def main():

    print("Elegí un grafo del 1 al 6")

    opcion = int(input("> "))

    grafo = obtener_grafo(opcion)

    if grafo is None:
        print("Opción inválida")
        return
    
    intentos_hasta_obtener_una_salida_valida = 0

    for _ in range(REINTENTOS_MAXIMOS):
        coloreo = colorear_grafo(grafo)
        total_aristas, satisfechas, no_satisfechas, cumple_condicion = obtener_metricas_coloreo(grafo, coloreo)

        if cumple_condicion:
            break

        intentos_hasta_obtener_una_salida_valida += 1

    print("\nColoreo generado:\n")

    for vertice in coloreo:
        print(f"Vertice {vertice} -> Color {coloreo[vertice]}")

    print(f"\nMétricas:")
    print(f"Total aristas: {total_aristas}")
    print(f"Aristas satisfecheas: {satisfechas}")
    print(f"Aristas no satisfecheas: {no_satisfechas}")
    print(f"2/3 del total de aristas están satisfechas: {"Si" if cumple_condicion else "No"}")
    print(f"Intentos hasta obtener una salida válida: {intentos_hasta_obtener_una_salida_valida}")

main()
    

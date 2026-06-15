from grafo import Grafo
from generador_grafos import obtener_grafo
from metricas import cumple_dos_tercios, metricas_coloreo

import random

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

    coloreo = colorear_grafo(grafo)
    satisfechas, no_satisfechas = metricas_coloreo(grafo, coloreo) # Aristas satisfechas
    total_aristas = satisfechas + no_satisfechas
    cumple_condicion = cumple_dos_tercios(grafo, coloreo)

    print("\nColoreo generado:\n")

    for vertice in coloreo:
        print(f"Vertice {vertice} -> Color {coloreo[vertice]}")

    print(f"\nMétricas:")
    print(f"Total aristas: {total_aristas}")
    print(f"Aristas satisfecheas: {satisfechas}")
    print(f"Aristas no satisfecheas: {no_satisfechas}")
    print(f"2/3 del total de aristas están satisfechas: {cumple_condicion}")

main()
    

from grafo import Grafo

def obtener_metricas_coloreo(grafo: Grafo, coloreo) -> tuple[int, int, int, bool]:

    satisfechas = 0
    no_satisfechas = 0

    visitadas = set()

    for v in grafo:

        for w in grafo.adyacentes(v):
            if (w, v) in visitadas:
                continue

            visitadas.add((v, w))

            if coloreo[v] != coloreo[w]:
                satisfechas += 1
            else:
                no_satisfechas += 1

    total_aristas = satisfechas + no_satisfechas
    cumple_coloreo = satisfechas >= (2 * total_aristas) / 3


    return total_aristas, satisfechas, no_satisfechas, cumple_coloreo


from grafo import Grafo

def metricas_coloreo(grafo: Grafo, coloreo):

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

    return satisfechas, no_satisfechas


def cumple_dos_tercios(grafo: Grafo, coloreo):

    satisfechas, no_satisfechas = metricas_coloreo(grafo, coloreo)

    total_aristas = satisfechas + no_satisfechas

    return "Sí" if satisfechas >= (2 * total_aristas) / 3 else "No"
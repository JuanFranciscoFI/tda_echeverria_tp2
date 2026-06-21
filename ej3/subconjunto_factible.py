import time
from leer_archivos import leer_archivo
# Algoritmo donde la se encuentra un subconjunto factible S menor o igual a la mitad de otro
# subconjunto factible con las mismas instancia A y B
def subconjunto_factible(A,B):
    A = sorted(A,reverse=True)
    S = []
    T = 0
    for a in A:
        if T + a <= B:
            S.append(a)
            T = T + a
    return S

def guardar_resultado(A, B, nombre_archivo):
    print(f"{len(A)}, {B}")
    print()
    t1 = time.perf_counter()
    resultado = subconjunto_factible(A, B)
    t2 = time.perf_counter()

    tiempo = t2 - t1

    with open(nombre_archivo, "w") as f:
        f.write(str(resultado) + "\n")
        f.write(str(tiempo) + "\n\n")

def main():
    A, B = leer_archivo("ej3/datos_de_entrada/entrada1.txt")
    guardar_resultado(A,B,"ej3/resultados/resultado1.txt")

    A, B = leer_archivo("ej3/datos_de_entrada/entrada2.txt")
    guardar_resultado(A,B,"ej3/resultados/resultado2.txt")

    A, B = leer_archivo("ej3/datos_de_entrada/entrada3.txt")
    guardar_resultado(A,B,"ej3/resultados/resultado3.txt")

    A, B = leer_archivo("ej3/datos_de_entrada/entrada4.txt")
    guardar_resultado(A,B,"ej3/resultados/resultado4.txt")

    A, B = leer_archivo("ej3/datos_de_entrada/entrada5.txt")
    guardar_resultado(A,B,"ej3/resultados/resultado5.txt")

main()
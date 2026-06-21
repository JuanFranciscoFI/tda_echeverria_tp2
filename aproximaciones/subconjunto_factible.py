import os
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    for i in range(1, 7):
        entrada = os.path.join(script_dir, f"datos_de_entrada/entrada{i}.txt")
        resultado = os.path.join(script_dir, f"resultados/resultado{i}.txt")
        A, B = leer_archivo(entrada)
        guardar_resultado(A, B, resultado)


main()
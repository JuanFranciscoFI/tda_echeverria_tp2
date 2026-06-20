import time

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

def imprimir_resultado(A,B):
    print(f"Para A = {A} y B = {B}")
    t1 = time.time()
    resultado =subconjunto_factible(A,B)
    t2 = time.time()
    print("Resultado: [", end="")
    print(", ".join(map(str, resultado)), end="")
    print("]")
    print("Tiempo: ", t2-t1)
    print()

def main():
    A = [10,20,80]
    B = 105
    imprimir_resultado(A,B)

    A = [51,50,50,50]
    B = 150
    imprimir_resultado(A,B)

    A = [55,54,50,50,40,40,40,30,30,20,20,10,15,5,10,15]
    B = sum(A)-4
    imprimir_resultado(A,B)

main()
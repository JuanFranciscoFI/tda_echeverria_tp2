def leer_archivo(nombre_archivo):
    with open(nombre_archivo, "r") as f:
        lineas = f.readlines()

    A = list(map(int, lineas[0].split()))
    B = int(lineas[1].strip())

    return A, B
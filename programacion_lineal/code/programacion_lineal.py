import pulp


def resolver_problema():
    # Crear el problema de maximización
    problema = pulp.LpProblem("Problema_1_Programacion_Lineal", pulp.LpMaximize)

    # Variables de decisión binarias
    x_A = pulp.LpVariable("A", cat="Binary")
    x_B80 = pulp.LpVariable("B_80", cat="Binary")
    x_B120 = pulp.LpVariable("B_120", cat="Binary")
    x_C = pulp.LpVariable("C", cat="Binary")
    x_D = pulp.LpVariable("D", cat="Binary")
    x_E = pulp.LpVariable("E", cat="Binary")
    x_F = pulp.LpVariable("F", cat="Binary")
    x_G = pulp.LpVariable("G", cat="Binary")

    # Función objetivo: maximizar beneficio total
    problema += (
        50000 * x_A +
        100000 * x_B80 +
        120000 * x_B120 +
        100000 * x_C +
        80000 * x_D +
        5000 * x_E +
        40000 * x_F +
        90000 * x_G
    ), "Beneficio_Total"

    # Restricción de capacidad máxima de paradas
    problema += (
        30 * x_A +
        80 * x_B80 +
        120 * x_B120 +
        75 * x_C +
        50 * x_D +
        2 * x_E +
        20 * x_F +
        100 * x_G
        <= 200
    ), "Capacidad_Maxima_Paradas"

    # Restricción: solo se puede elegir una opción del cliente B
    problema += x_B80 + x_B120 <= 1, "Unica_Opcion_B"

    # Restricción: A y D no pueden estar simultáneamente
    problema += x_A + x_D <= 1, "Incompatibilidad_A_D"

    # Resolver
    problema.solve(pulp.HiGHS(msg=False))

    # Calcular paradas utilizadas
    paradas_utilizadas = (
        30 * x_A.varValue +
        80 * x_B80.varValue +
        120 * x_B120.varValue +
        75 * x_C.varValue +
        50 * x_D.varValue +
        2 * x_E.varValue +
        20 * x_F.varValue +
        100 * x_G.varValue
    )

    # Mostrar resultados
    print("Estado:", pulp.LpStatus[problema.status])
    print("Beneficio total:", pulp.value(problema.objective))
    print()

    print("Variables seleccionadas:")
    for variable in problema.variables():
        print(f"{variable.name} = {variable.varValue}")

    print()
    print("Paradas utilizadas:", paradas_utilizadas)
    print("Paradas disponibles sin utilizar:", 200 - paradas_utilizadas)


if __name__ == "__main__":
    resolver_problema()
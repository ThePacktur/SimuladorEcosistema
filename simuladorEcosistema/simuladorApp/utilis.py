import numpy as np


def simular_seir(
    tasa_infeccion,
    tasa_incubacion,
    tasa_recuperacion,
    tasa_mortalidad,
    S0,
    E0,
    I0,
    R0,
    D0,
    dias,
):
    """Ejecuta una simulación SEIRD discreta.

    Las tasas deben estar en rango [0, 1] y representan probabilidades diarias.
    """
    S, E, I, R, D = [float(S0)], [float(E0)], [float(I0)], [float(R0)], [float(D0)]

    for _ in range(int(dias)):
        poblacion_viva = S[-1] + E[-1] + I[-1] + R[-1]
        if poblacion_viva <= 0:
            S.append(0.0)
            E.append(0.0)
            I.append(0.0)
            R.append(0.0)
            D.append(D[-1])
            continue

        nuevos_expuestos = min((tasa_infeccion * S[-1] * I[-1]) / poblacion_viva, S[-1])
        nuevos_infectados = min(tasa_incubacion * E[-1], E[-1])
        nuevos_recuperados = min(tasa_recuperacion * I[-1], I[-1])
        infectados_restantes = max(I[-1] - nuevos_recuperados, 0.0)
        nuevos_fallecidos = min(tasa_mortalidad * infectados_restantes, infectados_restantes)

        S_actual = max(S[-1] - nuevos_expuestos, 0.0)
        E_actual = max(E[-1] + nuevos_expuestos - nuevos_infectados, 0.0)
        I_actual = max(I[-1] + nuevos_infectados - nuevos_recuperados - nuevos_fallecidos, 0.0)
        R_actual = max(R[-1] + nuevos_recuperados, 0.0)
        D_actual = max(D[-1] + nuevos_fallecidos, 0.0)

        S.append(S_actual)
        E.append(E_actual)
        I.append(I_actual)
        R.append(R_actual)
        D.append(D_actual)

    return np.array(S), np.array(E), np.array(I), np.array(R), np.array(D)


# Compatibilidad hacia atrás con código existente
simularSeir = simular_seir

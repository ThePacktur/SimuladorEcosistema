import numpy as np

def simularSeir(tasaInfeccion, tasaRecuperacion, tasaMortalidad, S0, E0, I0, R0, D0, dias):
    S, E, I, R, D = [S0], [E0], [I0], [R0], [D0]
    N = S0 + E0 + I0 + R0 + D0  # Total de la población

    for _ in range(dias):
        nuevos_expuestos = (tasaInfeccion * S[-1] * I[-1]) / N
        nuevos_infectados = tasaRecuperacion * I[-1]
        nuevos_fallecidos = tasaMortalidad * I[-1]

        # Evitar valores negativos
        nuevos_expuestos = max(nuevos_expuestos, 0)
        nuevos_infectados = max(nuevos_infectados, 0)
        nuevos_fallecidos = max(nuevos_fallecidos, 0)

        S_actual = max(S[-1] - nuevos_expuestos, 0)
        E_actual = max(E[-1] + nuevos_expuestos - nuevos_infectados, 0)
        I_actual = max(I[-1] + nuevos_infectados - nuevos_infectados, 0)
        R_actual = max(R[-1] + nuevos_infectados, 0)
        D_actual = max(D[-1] + nuevos_fallecidos, 0)

        S.append(S_actual)
        E.append(E_actual)
        I.append(I_actual)
        R.append(R_actual)
        D.append(D_actual)

    return np.array(S), np.array(E), np.array(I), np.array(R), np.array(D)
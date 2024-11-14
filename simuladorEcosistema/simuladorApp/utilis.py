import numpy as np

#Este método simularSir devuelve matrices con los valores de S, I, y R a lo largo del tiempo.
def simularSir(beta,gamma,SO,IO,RO,tiempo):
    S, I, R = [SO], [IO], [RO] #lista para guardar los resultados en cada paso de tiempo

    for _ in range(tiempo):
        nuevo_S = S[-1] - (beta * S[-1] * I[-1])
        nuevo_I = I[-1] + (beta * S[-1] * I[-1]) - (gamma * I[-1])
        nuevo_R = R[-1] + (gamma * I[-1])

        S.append(nuevo_S)
        I.append(nuevo_I)
        R.append(nuevo_R)

    return np.array(S), np.array(I), np.array(R)

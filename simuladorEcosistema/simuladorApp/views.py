import base64
import io

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render

from .forms import ParametrosSimulacionForm
from .utilis import simular_seir

matplotlib.use("Agg")


def simulador(request):
    if request.method == "POST":
        form = ParametrosSimulacionForm(request.POST)
        if form.is_valid():
            tasa_infeccion = form.cleaned_data["tasaInfeccion"]
            tasa_recuperacion = form.cleaned_data["tasaRecuperacion"]
            tasa_mortalidad = form.cleaned_data["tasaMortalidad"]
            duracion_enfermedad = form.cleaned_data["duracionPromedioEnfermedad"]
            poblacion_inicial = form.cleaned_data["poblacionInicial"]
            infectados_inicial = form.cleaned_data["infectadosInicial"]
            tiempo_simulacion = form.cleaned_data["tiempoSimulacion"]

            # Aproximación de tasa de incubación diaria basada en duración promedio.
            tasa_incubacion = min(1 / duracion_enfermedad, 1)

            s0 = poblacion_inicial - infectados_inicial
            e0 = 0
            i0 = infectados_inicial
            r0 = 0
            d0 = 0

            S, E, I, R, D = simular_seir(
                tasa_infeccion=tasa_infeccion,
                tasa_incubacion=tasa_incubacion,
                tasa_recuperacion=tasa_recuperacion,
                tasa_mortalidad=tasa_mortalidad,
                S0=s0,
                E0=e0,
                I0=i0,
                R0=r0,
                D0=d0,
                dias=tiempo_simulacion,
            )

            recomendaciones = []
            if np.max(I) > poblacion_inicial * 0.2:
                recomendaciones.append("Implementar cuarentenas focalizadas para reducir la propagación.")
            if np.max(I) > 100:
                recomendaciones.append("Incrementar campañas de vacunación y diagnóstico temprano.")
            if tiempo_simulacion > 30:
                recomendaciones.append("Promover medidas de protección personal en espacios cerrados.")
            if I[-1] > I[0] * 1.5:
                recomendaciones.append("Reducir movilidad en zonas de alto contagio.")
            if np.max(R) < poblacion_inicial * 0.1:
                recomendaciones.append("Fortalecer la capacidad hospitalaria y protocolos de tratamiento.")
            if not recomendaciones:
                recomendaciones.append("El escenario es estable; mantener monitoreo y vigilancia epidemiológica.")

            plt.figure(figsize=(10, 5))
            dias = range(tiempo_simulacion + 1)
            plt.plot(dias, S, label="Susceptibles", color="blue")
            plt.plot(dias, E, label="Expuestos", color="orange")
            plt.plot(dias, I, label="Infectados", color="red")
            plt.plot(dias, R, label="Recuperados", color="green")
            plt.plot(dias, D, label="Fallecidos", color="black")
            plt.xlabel("Días")
            plt.ylabel("Población")
            plt.title("Simulación epidemiológica (SEIRD)")
            plt.legend()
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            plt.close()
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            buffer.close()

            tiempo_pico = int(np.argmax(I))
            porcentaje_infectados = round((float(np.max(I)) / poblacion_inicial) * 100, 2)
            porcentaje_recuperados = round((float(np.max(R)) / poblacion_inicial) * 100, 2)

            return render(
                request,
                "simuladorApp/resultados.html",
                {
                    "grafico": image_base64,
                    "recomendaciones": recomendaciones,
                    "tiempo_pico": tiempo_pico,
                    "porcentaje_infectados": porcentaje_infectados,
                    "porcentaje_recuperados": porcentaje_recuperados,
                },
            )
    else:
        form = ParametrosSimulacionForm()

    return render(request, "simuladorApp/simulador.html", {"form": form})

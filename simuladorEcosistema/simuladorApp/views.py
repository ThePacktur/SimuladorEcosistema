import base64
import io
from datetime import datetime, timezone

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import redirect, render

from .auth_views import login_required
from .firebase_service import list_simulations, save_simulation, get_simulation, firestore_available
from .forms import ParametrosSimulacionForm
from .utilis import simular_seir


@login_required
def dashboard(request):
    uid = request.session["uid"]
    role = request.session.get("rol", "estudiante")
    simulations = list_simulations(uid, role)
    return render(request, "simuladorApp/dashboard.html", {
        "simulaciones": simulations,
        "rol": role,
        "nombre": request.session.get("nombre", ""),
        "firebase_available": firestore_available(),
    })


@login_required
def simulador(request):
    if request.method == "POST":
        form = ParametrosSimulacionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            tasa_infeccion = data["tasaInfeccion"]
            tasa_recuperacion = data["tasaRecuperacion"]
            tasa_mortalidad = data["tasaMortalidad"]
            duracion_enfermedad = data["duracionPromedioEnfermedad"]
            poblacion_inicial = data["poblacionInicial"]
            infectados_inicial = data["infectadosInicial"]
            tiempo_simulacion = data["tiempoSimulacion"]
            asintomaticos = data["porcentajeAsintomaticos"]

            tasa_incubacion = min(1 / duracion_enfermedad, 1)

            s0 = poblacion_inicial - infectados_inicial
            S, E, I, R, D = simular_seir(
                tasa_infeccion=tasa_infeccion,
                tasa_incubacion=tasa_incubacion,
                tasa_recuperacion=tasa_recuperacion,
                tasa_mortalidad=tasa_mortalidad,
                S0=s0,
                E0=0,
                I0=infectados_inicial,
                R0=0,
                D0=0,
                dias=tiempo_simulacion,
            )

            max_infectados = float(np.max(I))
            max_recuperados = float(np.max(R))
            max_fallecidos = float(np.max(D))
            pico = int(np.argmax(I))
            casos_sintomaticos = I * (1 - asintomaticos / 100)
            casos_asintomaticos = I * (asintomaticos / 100)

            recomendaciones = []
            if max_infectados > poblacion_inicial * 0.2:
                recomendaciones.append("Implementar medidas de aislamiento focalizado para reducir la propagación.")
            if max_infectados > 100:
                recomendaciones.append("Reforzar campañas de vacunación y diagnóstico temprano.")
            if tiempo_simulacion > 30:
                recomendaciones.append("Promover medidas de protección personal en espacios cerrados.")
            if I[-1] > I[0] * 1.5:
                recomendaciones.append("Reducir movilidad en zonas de alta transmisión.")
            if max_recuperados < poblacion_inicial * 0.1:
                recomendaciones.append("Revisar capacidad de respuesta y seguimiento de casos.")
            if not recomendaciones:
                recomendaciones.append("El escenario es estable; mantener monitoreo epidemiológico.")

            plt.figure(figsize=(11, 5))
            dias = range(tiempo_simulacion + 1)
            plt.plot(dias, S, label="Susceptibles")
            plt.plot(dias, E, label="Expuestos")
            plt.plot(dias, I, label="Infectados")
            plt.plot(dias, R, label="Recuperados")
            plt.plot(dias, D, label="Fallecidos")
            plt.xlabel("Días")
            plt.ylabel("Población")
            plt.title(f"Simulación SEIRD - {data['virus']}")
            plt.legend()
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", dpi=130)
            plt.close()
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            buffer.close()

            resultado = {
                "dias": tiempo_simulacion,
                "maxInfectados": round(max_infectados, 2),
                "maxRecuperados": round(max_recuperados, 2),
                "maxFallecidos": round(max_fallecidos, 2),
                "diaPico": pico,
                "porcentajeInfectados": round(max_infectados / poblacion_inicial * 100, 2),
                "porcentajeRecuperados": round(max_recuperados / poblacion_inicial * 100, 2),
                "porcentajeFallecidos": round(max_fallecidos / poblacion_inicial * 100, 2),
                "sintomaticosPico": round(float(np.max(casos_sintomaticos)), 2),
                "asintomaticosPico": round(float(np.max(casos_asintomaticos)), 2),
                "grafico": image_base64,
            }

            simulation = {
                "usuarioId": request.session["uid"],
                "usuarioNombre": request.session.get("nombre", ""),
                "enfermedad": data["virus"],
                "nombreEscenario": data["nombreEscenario"],
                "poblacion": poblacion_inicial,
                "edadMin": data["edadMin"],
                "edadMax": data["edadMax"],
                "porcentajeAsintomaticos": asintomaticos,
                "parametros": {
                    "tasaInfeccion": tasa_infeccion,
                    "tasaRecuperacion": tasa_recuperacion,
                    "tasaMortalidad": tasa_mortalidad,
                    "duracionPromedioEnfermedad": duracion_enfermedad,
                    "infectadosInicial": infectados_inicial,
                    "tiempoSimulacion": tiempo_simulacion,
                },
                "resultado": resultado,
                "recomendaciones": recomendaciones,
                "fecha": datetime.now(timezone.utc).isoformat(),
            }

            simulation_id = save_simulation(simulation)

            return render(request, "simuladorApp/resultados.html", {
                "grafico": image_base64,
                "recomendaciones": recomendaciones,
                "resultado": resultado,
                "simulation_id": simulation_id,
                "virus": data["virus"],
                "nombre_escenario": data["nombreEscenario"],
                "edad_min": data["edadMin"],
                "edad_max": data["edadMax"],
                "porcentaje_asintomaticos": asintomaticos,
            })
    else:
        form = ParametrosSimulacionForm()

    return render(request, "simuladorApp/simulador.html", {"form": form})


@login_required
def revisar_simulacion(request, simulation_id):
    simulation = get_simulation(
        simulation_id,
        request.session["uid"],
        request.session.get("rol", "estudiante"),
    )
    if not simulation:
        return redirect("dashboard")
    return render(request, "simuladorApp/revisar.html", {"simulation": simulation})


@login_required
def comparar(request):
    role = request.session.get("rol", "estudiante")
    simulations = list_simulations(request.session["uid"], role)
    selected = request.GET.getlist("id")
    comparadas = [s for s in simulations if s["id"] in selected][:4]
    return render(request, "simuladorApp/comparar.html", {
        "simulaciones": simulations,
        "comparadas": comparadas,
        "rol": role,
    })


def educacion(request):
    contenidos = [
        {"titulo": "Prevención de infecciones", "texto": "Lavado de manos, ventilación, etiqueta respiratoria y vacunación son medidas de prevención que deben evaluarse según la enfermedad y el contexto."},
        {"titulo": "Aislamiento", "texto": "Las precauciones de aislamiento dependen del mecanismo de transmisión. En un contexto académico se deben contrastar siempre con las normas y protocolos oficiales vigentes."},
        {"titulo": "Cuándo buscar atención", "texto": "Ante dificultad respiratoria, deterioro importante del estado general, signos de deshidratación u otros síntomas de alarma, se debe buscar evaluación profesional. Esta pantalla entrega orientación general y no reemplaza una evaluación médica."},
    ]
    return render(request, "simuladorApp/educacion.html", {"contenidos": contenidos})

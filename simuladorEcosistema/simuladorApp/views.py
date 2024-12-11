from django.shortcuts import render
from .serializers import ParametroSimulacionSerializer
from rest_framework import status, viewsets
from .forms import ParametrosSimulacionForm
from .models import ParametrosSimulacion

import matplotlib.pyplot as plt
from simuladorApp.utilis import simularSeir
import numpy as np
import io
import base64
def simulador(request):
    if request.method == 'POST':
        form = ParametrosSimulacionForm(request.POST)
        if form.is_valid():
            # Obtener datos validados del formulario
            tasaInfeccion = form.cleaned_data['tasaInfeccion']
            tasaRecuperacion = form.cleaned_data['tasaRecuperacion']
            poblacionInicial = form.cleaned_data['poblacionInicial']
            infectadosInicial = form.cleaned_data['infectadosInicial']
            tiempoSimulacion = form.cleaned_data['tiempoSimulacion']
            intervenciones = form.cleaned_data.get('intervenciones', [])

            # Implementar lógicas de intervenciones
            if 'mascarillas' in intervenciones:
                tasaInfeccion *= 0.8  # Reducción del 20% por uso de mascarillas

            # Configuración inicial
            SO = poblacionInicial - infectadosInicial
            IO = infectadosInicial
            RO = 0  # Recuperados iniciales
            D0 = 0  # Muertos iniciales
            E0 = 0  # Expuestos iniciales (esto depende de tu modelo, puedes ajustarlo si es necesario)
            tasaMortalidad = 0.01  # Definir tasa de mortalidad (ajusta este valor según sea necesario)

            # Ejecutar simulación
            S, E, I, R, D = simularSeir(tasaInfeccion, tasaRecuperacion, tasaMortalidad, SO, E0, IO, RO, D0, tiempoSimulacion)

            # Generar recomendaciones dinámicas basadas en la simulación
            recomendaciones = []

            # Si el número de infectados es muy alto
            if max(I) > poblacionInicial * 0.2:
                recomendaciones.append("Implementar cuarentenas estrictas para reducir la propagación.")

            # Si el número de infectados supera cierto umbral
            if max(I) > 100:
                recomendaciones.append("Incrementar campañas de vacunación.")

            # Si la simulación es de más de 30 días, recomendar uso de mascarillas
            if tiempoSimulacion > 30:
                recomendaciones.append("Promover el uso de mascarillas en espacios cerrados.")

            # Nuevas recomendaciones basadas en el comportamiento observado
            # Si la curva de infectados sigue creciendo rápidamente, sugerir restricciones de viajes
            if I[-1] > I[0] * 2:
                recomendaciones.append("Restricciones de viajes para evitar propagación masiva.")

            # Si el número de recuperados es bajo, sugerir mejorar tratamientos
            if max(R) < poblacionInicial * 0.1:
                recomendaciones.append("Revisar estrategias de tratamiento y hospitalización.")

            # Graficar resultado
            plt.figure(figsize=(10, 5))
            plt.plot(range(tiempoSimulacion + 1), S, label="Susceptibles", color="blue")
            plt.plot(range(tiempoSimulacion + 1), I, label="Infectados", color="red")
            plt.plot(range(tiempoSimulacion + 1), R, label="Recuperados", color="green")
            plt.xlabel("Días")
            plt.ylabel("Población")
            plt.title("Simulación Epidemiológica")
            plt.legend()

            # Guardar la imagen como base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            imagen_png = buffer.getvalue()
            buffer.close()
            image_base64 = base64.b64encode(imagen_png).decode('utf-8')

            # Después de calcular las simulaciones
            tiempo_pico = np.argmax(I)  # Primer índice donde I alcanza su máximo
            porcentaje_infectados = (max(I) / poblacionInicial) * 100
            porcentaje_recuperados = (max(R) / poblacionInicial) * 100

            return render(request, 'simuladorApp/resultados.html', {
                'grafico': image_base64,
                'recomendaciones': recomendaciones,
                'tiempo_pico': tiempo_pico,
                'porcentaje_infectados': porcentaje_infectados,
                'porcentaje_recuperados': porcentaje_recuperados,
            })
    else:
        form = ParametrosSimulacionForm()

    return render(request, 'simuladorApp/simulador.html', {'form': form})
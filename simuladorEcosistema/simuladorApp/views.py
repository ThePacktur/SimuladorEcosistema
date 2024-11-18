from django.shortcuts import render
from .forms import ParametrosSimulacionForm
from .utilis import simularSir
import matplotlib.pyplot as plt
import io
import base64

def simulador(request):
    if request.method == 'POST':
        form = ParametrosSimulacionForm(request.POST)
        if form.is_valid():
            # Obtener datos del formulario
            tasaInfeccion = form.cleaned_data['tasaInfeccion']
            tasaRecuperacion = form.cleaned_data['tasaRecuperacion']
            poblacionInicial = form.cleaned_data['poblacionInicial']
            infectadosInicial = form.cleaned_data['infectadosInicial']
            tiempoSimulacion = form.cleaned_data['tiempoSimulacion']

            # Configuración inicial
            SO = poblacionInicial - infectadosInicial
            IO = infectadosInicial
            RO = 0

            # Ejecuta la simulación
            S, I, R = simularSir(tasaInfeccion, tasaRecuperacion, SO, IO, RO, tiempoSimulacion)

            # Generar recomendaciones
            recomendaciones = []
            if max(I) > poblacionInicial * 0.2:
                recomendaciones.append("Implementar cuarentenas estrictas para reducir la propagación.")
            if max(I) > 100:
                recomendaciones.append("Incrementar campañas de vacunación.") #agregar plan de vacunacion previa a a la propagacion de la enfermedad
            if len(S) > 30:
                recomendaciones.append("Promover el uso de mascarillas en espacios cerrados.")
            
            # Graficar el resultado
            plt.figure(figsize=(10, 5))
            plt.plot(S, label="Susceptibles", color="blue")
            plt.plot(I, label="Infectados", color="red")
            plt.plot(R, label="Recuperados", color="green")
            plt.xlabel("Días")
            plt.ylabel("Población")
            plt.title("Simulación Epidemiológica")
            plt.legend()

            # Guardar la imagen como PNG
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            imagen_png = buffer.getvalue()
            buffer.close()
            image_base64 = base64.b64encode(imagen_png).decode('utf-8')

            return render(request, 'simuladorApp/resultados.html', {
                'grafico': image_base64,
                'recomendaciones': recomendaciones
            })
    else:
        form = ParametrosSimulacionForm()

    return render(request, 'simuladorApp/simulador.html', {'form': form})

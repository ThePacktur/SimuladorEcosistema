from django.shortcuts import render
from .models import ParametrosSimulacion
from .utilis import simularSir
import matplotlib.pyplot as plt
import io
import base64

# Create your views here.

def simulador(request):
    if request.method == 'POST':
        # obten los parametros desde el formulario
        tasaInfeccion = float(request.POST['tasaInfeccion'])
        tasaRecuperacion = float(request.POST['tasaRecuperacion'])
        poblacionInicial = int(request.POST['poblacionInicial'])
        infectadosInicial = int(request.POST['infectadosInicial'])
        tiempoSimulacion = int(request.POST['tiempoSimulacion'])

        #Configuracion inicual
        SO = poblacionInicial - infectadosInicial
        IO = infectadosInicial
        RO = 0

        #ejecuta la simulacion
        S,I,R = simularSir(tasaInfeccion,tasaRecuperacion,SO,IO,RO, tiempoSimulacion)

        #Graficar el resultado
        plt.figure(figsize=(10,5))
        plt.plot(S, label="Susceptibles")
        plt.plot(I, label="Infectados")
        plt.plot(R, label="Recuperados")
        plt.xlabel("Dias")
        plt.ylabel("Poblacion")
        plt.legend()

        #Guardar la imagen como PNG
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_png = buffer.getvalue()
        buffer.close()
        image_base64 = base64.b64encode(imagen_png).decode('utf-8')
        return render(request,'simuladorApp/resultados.html',{'grafico': image_base64})
    else:
        return render(request,'simuladorApp/simulador.html')
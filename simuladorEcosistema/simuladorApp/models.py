from django.db import models

# Create your models here.
class ParametrosSimulacion(models.Model):
    tasaInfeccion = models.FloatField()
    tasaRecuperacion = models.FloatField()
    tasaMortalidad = models.FloatField()
    duracionPromedioEnfermedad = models.IntegerField()  # en días
    poblacionInicial = models.IntegerField()
    infectadosInicial = models.IntegerField()
    tiempoSimulacion = models.IntegerField()
    
    def __str__(self):
        return f"Simulación con β={self.tasaInfeccion}, γ={self.tasaRecuperacion}, mortalidad={self.tasaMortalidad}"
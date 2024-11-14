from django.db import models

# Create your models here.

class ParametrosSimulacion(models.Model):
    tasaInfeccion = models.FloatField()
    tasaRecuperacion = models.FloatField()
    poblacionInicial = models.IntegerField()
    infectadosInicial = models.IntegerField()
    tiempoSimulacion = models.IntegerField()


def __str__(self):
    return f"Simulacion con  β={self.tasa_infeccion}, γ={self.tasa_recuperacion} "

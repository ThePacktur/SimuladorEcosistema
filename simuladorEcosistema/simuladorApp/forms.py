from django import forms
from .models import ParametrosSimulacion

class ParametrosSimulacionForm(forms.ModelForm):
   
    class Meta:
        model = ParametrosSimulacion
        fields = ['tasaInfeccion', 'tasaRecuperacion', 'tasaMortalidad', 'duracionPromedioEnfermedad', 'poblacionInicial', 'infectadosInicial', 'tiempoSimulacion']
        widgets = {
            'tasaInfeccion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasaRecuperacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasaMortalidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'duracionPromedioEnfermedad': forms.NumberInput(attrs={'class': 'form-control'}),
            'poblacionInicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'infectadosInicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'tiempoSimulacion': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_tasaInfeccion(self):
        tasa_infeccion = self.cleaned_data.get('tasaInfeccion')
        if tasa_infeccion < 0:
            raise forms.ValidationError("La tasa de infección no puede ser negativa.")
        return tasa_infeccion

    def clean_tasaRecuperacion(self):
        tasa_recuperacion = self.cleaned_data.get('tasaRecuperacion')
        if tasa_recuperacion < 0:
            raise forms.ValidationError("La tasa de recuperación no puede ser negativa.")
        return tasa_recuperacion

    def clean_poblacionInicial(self):
        poblacion_inicial = self.cleaned_data.get('poblacionInicial')
        if poblacion_inicial <= 0:
            raise forms.ValidationError("La población inicial debe ser un número positivo.")
        return poblacion_inicial

    def clean_infectadosInicial(self):
        infectados_inicial = self.cleaned_data.get('infectadosInicial')
        poblacion_inicial = self.cleaned_data.get('poblacionInicial')
        if infectados_inicial < 0:
            raise forms.ValidationError("El número de infectados iniciales no puede ser negativo.")
        if poblacion_inicial and infectados_inicial >= poblacion_inicial:
            raise forms.ValidationError("El número de infectados iniciales no puede ser igual o superior a la población inicial.")
        return infectados_inicial

    def clean_tiempoSimulacion(self):
        tiempo_simulacion = self.cleaned_data.get('tiempoSimulacion')
        if tiempo_simulacion <= 0:
            raise forms.ValidationError("El tiempo de simulación debe ser un número positivo.")
        return tiempo_simulacion
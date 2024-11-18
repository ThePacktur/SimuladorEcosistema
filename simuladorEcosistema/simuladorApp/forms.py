from django import forms
from .models import ParametrosSimulacion

class ParametrosSimulacionForm(forms.ModelForm):
    class Meta:
        model = ParametrosSimulacion
        fields = ['tasaInfeccion', 'tasaRecuperacion', 'poblacionInicial', 'infectadosInicial', 'tiempoSimulacion']
        widgets = {
            'tasaInfeccion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasaRecuperacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'poblacionInicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'infectadosInicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'tiempoSimulacion': forms.NumberInput(attrs={'class': 'form-control'}),
        }

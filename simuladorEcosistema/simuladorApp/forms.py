from django import forms

from .models import ParametrosSimulacion


class ParametrosSimulacionForm(forms.ModelForm):
    class Meta:
        model = ParametrosSimulacion
        fields = [
            "tasaInfeccion",
            "tasaRecuperacion",
            "tasaMortalidad",
            "duracionPromedioEnfermedad",
            "poblacionInicial",
            "infectadosInicial",
            "tiempoSimulacion",
        ]
        widgets = {
            "tasaInfeccion": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0", "max": "1"}),
            "tasaRecuperacion": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0", "max": "1"}),
            "tasaMortalidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0", "max": "1"}),
            "duracionPromedioEnfermedad": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "poblacionInicial": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "infectadosInicial": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "tiempoSimulacion": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
        }

    def _validar_tasa(self, campo, etiqueta):
        tasa = self.cleaned_data.get(campo)
        if tasa is None:
            return tasa
        if not 0 <= tasa <= 1:
            raise forms.ValidationError(f"La {etiqueta} debe estar entre 0 y 1.")
        return tasa

    def clean_tasaInfeccion(self):
        return self._validar_tasa("tasaInfeccion", "tasa de infección")

    def clean_tasaRecuperacion(self):
        return self._validar_tasa("tasaRecuperacion", "tasa de recuperación")

    def clean_tasaMortalidad(self):
        return self._validar_tasa("tasaMortalidad", "tasa de mortalidad")

    def clean(self):
        cleaned_data = super().clean()
        poblacion = cleaned_data.get("poblacionInicial")
        infectados = cleaned_data.get("infectadosInicial")
        duracion = cleaned_data.get("duracionPromedioEnfermedad")

        if poblacion is not None and poblacion <= 0:
            self.add_error("poblacionInicial", "La población inicial debe ser mayor que cero.")

        if infectados is not None and infectados <= 0:
            self.add_error("infectadosInicial", "Los infectados iniciales deben ser mayores que cero.")

        if (
            poblacion is not None
            and infectados is not None
            and infectados >= poblacion
        ):
            self.add_error(
                "infectadosInicial",
                "El número de infectados iniciales debe ser menor que la población inicial.",
            )

        if duracion is not None and duracion <= 0:
            self.add_error(
                "duracionPromedioEnfermedad",
                "La duración promedio de enfermedad debe ser mayor que cero.",
            )

        return cleaned_data

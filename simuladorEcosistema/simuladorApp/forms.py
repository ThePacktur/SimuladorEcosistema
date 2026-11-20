from django import forms


VIRUS_CHOICES = [
    ("Virus respiratorio sincicial (VRS)", "Virus respiratorio sincicial (VRS)"),
    ("Influenza", "Influenza"),
    ("COVID-19", "COVID-19"),
    ("Sarampión", "Sarampión"),
    ("Otro", "Otro"),
]


class ParametrosSimulacionForm(forms.Form):
    nombreEscenario = forms.CharField(
        label="Nombre del escenario",
        max_length=80,
        initial="Escenario de simulación",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: VRS invierno 2026"}),
    )
    virus = forms.ChoiceField(
        label="Virus o enfermedad",
        choices=VIRUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    tasaInfeccion = forms.FloatField(
        label="Tasa de infección",
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )
    tasaRecuperacion = forms.FloatField(
        label="Tasa de recuperación",
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )
    tasaMortalidad = forms.FloatField(
        label="Tasa de mortalidad",
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.001"}),
    )
    duracionPromedioEnfermedad = forms.IntegerField(
        label="Duración promedio de enfermedad (días)",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
    )
    poblacionInicial = forms.IntegerField(
        label="Población inicial",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
    )
    infectadosInicial = forms.IntegerField(
        label="Infectados iniciales",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
    )
    tiempoSimulacion = forms.IntegerField(
        label="Tiempo de simulación (días)",
        min_value=1,
        max_value=3650,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "1", "max": "3650"}),
    )
    edadMin = forms.IntegerField(
        label="Edad mínima",
        min_value=0,
        max_value=120,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "0", "max": "120"}),
    )
    edadMax = forms.IntegerField(
        label="Edad máxima",
        min_value=0,
        max_value=120,
        initial=100,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "0", "max": "120"}),
    )
    porcentajeAsintomaticos = forms.FloatField(
        label="Porcentaje estimado de casos asintomáticos",
        min_value=0,
        max_value=100,
        initial=20,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "1", "min": "0", "max": "100"}),
    )

    def clean(self):
        cleaned = super().clean()
        poblacion = cleaned.get("poblacionInicial")
        infectados = cleaned.get("infectadosInicial")
        edad_min = cleaned.get("edadMin")
        edad_max = cleaned.get("edadMax")

        if poblacion and infectados and infectados >= poblacion:
            self.add_error("infectadosInicial", "Los infectados iniciales deben ser menores que la población.")

        if edad_min is not None and edad_max is not None and edad_min > edad_max:
            self.add_error("edadMin", "La edad mínima no puede ser mayor que la edad máxima.")

        tasas = ["tasaInfeccion", "tasaRecuperacion", "tasaMortalidad"]
        for campo in tasas:
            value = cleaned.get(campo)
            if value is not None and not 0 <= value <= 1:
                self.add_error(campo, "El valor debe estar entre 0 y 1.")

        return cleaned

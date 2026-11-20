from django.test import TestCase
from django.urls import reverse

from .forms import ParametrosSimulacionForm
from .utilis import simular_seir


class SimulacionSEIRTests(TestCase):
    def test_simulacion_conserva_poblacion_total(self):
        S,E,I,R,D=simular_seir(
            tasa_infeccion=0.4,tasa_incubacion=0.2,tasa_recuperacion=0.1,
            tasa_mortalidad=0.01,S0=990,E0=0,I0=10,R0=0,D0=0,dias=30
        )
        self.assertAlmostEqual(S[0]+E[0]+I[0]+R[0]+D[0],S[-1]+E[-1]+I[-1]+R[-1]+D[-1],places=6)


class FormularioTests(TestCase):
    def test_formulario_invalido_con_tasa_fuera_de_rango(self):
        form=ParametrosSimulacionForm(data={
            "nombreEscenario":"Prueba","virus":"Influenza",
            "tasaInfeccion":1.2,"tasaRecuperacion":0.1,"tasaMortalidad":0.01,
            "duracionPromedioEnfermedad":7,"poblacionInicial":1000,
            "infectadosInicial":10,"tiempoSimulacion":40,
            "edadMin":0,"edadMax":100,"porcentajeAsintomaticos":20
        })
        self.assertFalse(form.is_valid())
        self.assertIn("tasaInfeccion",form.errors)


class VistaSimuladorTests(TestCase):
    def setUp(self):
        session=self.client.session
        session["uid"]="test-uid"
        session["email"]="test@example.com"
        session["nombre"]="Estudiante de prueba"
        session["rol"]="estudiante"
        session.save()

    def test_get_simulador_responde_200(self):
        response=self.client.get(reverse("simulador"))
        self.assertEqual(response.status_code,200)

    def test_login_redirige_si_no_hay_sesion(self):
        self.client.session.flush()
        response=self.client.get(reverse("simulador"))
        self.assertEqual(response.status_code,302)\n        self.assertEqual(response.url,reverse("login"))

    def test_post_simulador_renderiza_resultados(self):
        response=self.client.post(reverse("simulador"),data={
            "nombreEscenario":"Prueba VRS","virus":"Virus respiratorio sincicial (VRS)",
            "tasaInfeccion":0.35,"tasaRecuperacion":0.1,"tasaMortalidad":0.02,
            "duracionPromedioEnfermedad":7,"poblacionInicial":1000,
            "infectadosInicial":5,"tiempoSimulacion":20,
            "edadMin":0,"edadMax":14,"porcentajeAsintomaticos":20
        })
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Resultados")

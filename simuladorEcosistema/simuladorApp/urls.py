from django.urls import path
from . import views, auth_views
urlpatterns=[
path("",views.dashboard,name="dashboard"),path("dashboard/",views.dashboard,name="dashboard"),
path("simulador/",views.simulador,name="simulador"),path("revisar/<str:simulation_id>/",views.revisar_simulacion,name="revisar_simulacion"),
path("comparar/",views.comparar,name="comparar"),path("educacion/",views.educacion,name="educacion"),
path("login/",auth_views.login_view,name="login"),path("registro/",auth_views.register_view,name="registro"),
path("api/login/firebase/",auth_views.firebase_login,name="firebase_login"),path("api/registro/firebase/",auth_views.firebase_register,name="firebase_register"),
path("api/perfil/firebase/",auth_views.firebase_profile,name="firebase_profile"),path("logout/",auth_views.logout_view,name="logout")]
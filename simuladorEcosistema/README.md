# Simulador de Ecosistema Epidemiológico (SEIRD)

Aplicación web educativa para simular la evolución de enfermedades infecciosas mediante un modelo SEIRD.

## Historias de usuario implementadas

- Inicio de sesión y registro con Firebase Authentication.
- Ejecución de simulaciones SEIRD.
- Configuración de población y rango etario.
- Estimación de casos sintomáticos y asintomáticos.
- Visualización de evolución mediante gráfico SEIRD.
- Indicadores epidemiológicos.
- Creación de escenarios.
- Revisión de simulaciones propias y, para docentes/admin, simulaciones de estudiantes.
- Comparación de hasta cuatro escenarios.
- Contenido educativo sobre prevención, aislamiento y orientación general.

## Arquitectura

Frontend: Django Templates + Bootstrap + JavaScript.  
Backend: Django + motor SEIRD en Python/NumPy.  
Autenticación: Firebase Authentication.  
Persistencia: Cloud Firestore (NoSQL).  
Sesión del servidor: Django Session, iniciada después de verificar el ID token de Firebase con Firebase Admin SDK.

Flujo:

Usuario → Firebase Authentication → Django → motor SEIRD → Firestore → resultados

## Instalación local

```bash
cd simuladorEcosistema
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Firebase

1. Crea un proyecto en Firebase.
2. Habilita Authentication → Sign-in method → Email/Password.
3. Crea una aplicación Web y copia su configuración en .env.
4. Genera una cuenta de servicio y guarda el JSON fuera del repositorio.
5. Configura las variables de .env.example.
6. Configura Firestore y aplica firebase.rules.
7. Inicia Django.

Nunca subas el JSON de la cuenta de servicio a GitHub.

## Nota sobre procedimientos almacenados

Firestore es NoSQL y no utiliza procedimientos almacenados SQL. En este proyecto las operaciones equivalentes se encapsulan en firebase_service.py y las restricciones de acceso se aplican con reglas de Firestore. Si la rúbrica exige literalmente un procedimiento almacenado SQL, debe documentarse esta incompatibilidad o incorporarse un servicio relacional separado; no corresponde llamar procedimiento almacenado a una consulta Firestore.

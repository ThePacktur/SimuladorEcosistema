# Simulador de Ecosistema Epidemiológico (SEIRD)

Aplicación web educativa desarrollada con **Django** para representar y analizar escenarios de propagación de enfermedades infecciosas mediante un modelo **SEIRD**. El sistema está orientado al aprendizaje de epidemiología y no reemplaza diagnósticos, decisiones clínicas ni modelos epidemiológicos profesionales.

## Índice

- Descripción
- Funcionalidades
- Historias de usuario
- Arquitectura
- Tecnologías
- Estructura del proyecto
- Requisitos
- Instalación local
- Configuración de Firebase
- Ejecución
- Uso del sistema
- Roles y permisos
- Seguridad
- Pruebas
- Despliegue
- Limitaciones
- Solución de problemas
- Rúbrica y decisiones técnicas

## Descripción

El sistema permite configurar una población y ejecutar escenarios de propagación. La simulación calcula la evolución diaria de cinco grupos:

| Estado | Significado |
|---|---|
| **S** | Susceptibles |
| **E** | Expuestos |
| **I** | Infectados |
| **R** | Recuperados |
| **D** | Fallecidos |

El objetivo es visualizar la evolución del escenario y obtener indicadores que faciliten su interpretación.

> **Importante:** los resultados son simulaciones académicas. Los parámetros ingresados por el usuario no representan automáticamente datos epidemiológicos oficiales.

## Funcionalidades

- Registro e inicio de sesión mediante **Firebase Authentication**.
- Perfil de usuario almacenado en **Cloud Firestore**.
- Ejecución de simulaciones SEIRD.
- Configuración de población e infectados iniciales.
- Configuración de rango etario.
- Selección de virus o enfermedad.
- Estimación de casos sintomáticos y asintomáticos.
- Gráfico de evolución S, E, I, R y D.
- Indicadores de pico de infectados, recuperados y fallecidos.
- Recomendaciones automáticas según el escenario.
- Guardado de escenarios en Firestore.
- Revisión de simulaciones propias.
- Revisión de simulaciones de estudiantes para perfiles docentes y administrativos.
- Comparación de hasta cuatro escenarios.
- Material educativo sobre prevención, aislamiento y orientación general.
- Protección de rutas mediante sesión de Django.
- Validación de parámetros antes de ejecutar una simulación.

## Historias de usuario

| ID | Historia | Prioridad | Estado |
|---|---|---|---|
| HU-01 | Iniciar sesión | Muy alta | Implementada |
| HU-02 | Ejecutar simulación | Muy alta | Implementada |
| HU-03 | Configurar población y rango etario | Muy alta | Implementada |
| HU-04 | Visualizar casos sintomáticos y asintomáticos | Alta | Implementada |
| HU-05 | Visualizar evolución mediante gráficos | Muy alta | Implementada |
| HU-06 | Visualizar indicadores epidemiológicos | Muy alta | Implementada |
| HU-07 | Crear escenarios de simulación | Alta | Implementada |
| HU-08 | Revisar simulaciones de estudiantes | Alta | Implementada para docente/admin |
| HU-09 | Comparar resultados | Media | Implementada |
| HU-10 | Consultar prevención y aislamiento | Media | Implementada |
| HU-11 | Seleccionar virus/enfermedad | Media | Implementada |
| HU-12 | Orientación general sobre atención médica | Media | Implementada |

## Arquitectura

La solución utiliza Django como capa web y separa presentación, lógica de aplicación, autenticación y persistencia.

```
┌──────────────────────────────────┐
│ Navegador                        │
│ HTML + Bootstrap + JavaScript    │
└───────────────┬──────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│ Django                           │
│ URLs + Views + Forms + Sesiones  │
└───────────────┬──────────────────┘
                │
       ┌────────┴──────────┐
       ▼                   ▼
┌───────────────┐   ┌──────────────────┐
│ Motor SEIRD   │   │ Firebase Admin    │
│ Python/NumPy  │   │ Authentication   │
│ + Matplotlib  │   └────────┬─────────┘
└───────────────┘            │
                             ▼
                    ┌──────────────────┐
                    │ Cloud Firestore   │
                    │ Base NoSQL        │
                    └──────────────────┘
```

### Flujo de autenticación

1. El usuario se registra o inicia sesión con Firebase Authentication.
2. Firebase entrega un ID token.
3. El navegador envía el token a Django.
4. Django lo valida mediante Firebase Admin SDK.
5. Django crea una sesión de servidor con UID, nombre, correo y rol.
6. Las rutas protegidas verifican esa sesión.

### Flujo de simulación

1. El usuario completa los parámetros.
2. Django valida los datos mediante `ParametrosSimulacionForm`.
3. `simular_seir()` calcula la evolución diaria.
4. Matplotlib genera el gráfico.
5. Django calcula indicadores y recomendaciones.
6. El escenario se guarda en Firestore.
7. Se muestran los resultados al usuario.

## Tecnologías

- **Python 3.10+**
- **Django 5**
- **NumPy**
- **Matplotlib**
- **Firebase Authentication**
- **Cloud Firestore (NoSQL)**
- **Firebase Admin SDK**
- **Bootstrap 5**
- **JavaScript ES Modules**
- **Gunicorn** para despliegue WSGI

## Estructura del proyecto

```
SimuladorEcosistema/
├── README.md
└── simuladorEcosistema/
    ├── manage.py
    ├── requirements.txt
    ├── .env.example
    ├── firebase.rules
    ├── simuladorEcosistema/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── simuladorApp/
    │   ├── auth_views.py
    │   ├── firebase_service.py
    │   ├── forms.py
    │   ├── tests.py
    │   ├── utilis.py
    │   └── views.py
    ├── templates/
    │   └── simuladorApp/
    └── static/
        ├── app.css
        └── auth.js
```

## Requisitos

- Python **3.10 o superior**.
- pip.
- Cuenta de Firebase/Google.
- Proyecto Firebase con Authentication y Firestore habilitados.
- Navegador moderno con soporte para JavaScript ES Modules.

## Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/ThePacktur/SimuladorEcosistema.git
cd SimuladorEcosistema/simuladorEcosistema
```

### 2. Crear entorno virtual

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows CMD:**

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia `.env.example` como `.env` y completa sus valores.

> Django no carga archivos `.env` automáticamente. Para desarrollo puedes exportar las variables desde el sistema. En producción se recomienda utilizar las variables de entorno o secretos del proveedor de hosting.

Ejemplo en PowerShell:

```powershell
$env:DJANGO_SECRET_KEY="una-clave-local-larga"
$env:DJANGO_DEBUG="True"
$env:DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
```

Las variables de Firebase se explican a continuación.

### 5. Migraciones de Django

Aunque las simulaciones se almacenan en Firestore, Django utiliza SQLite para sus componentes internos.

```bash
python manage.py migrate
```

### 6. Ejecutar

```bash
python manage.py runserver
```

Abrir en el navegador:

```
http://127.0.0.1:8000/
```

## Configuración de Firebase

### 1. Crear el proyecto

En Firebase Console:

1. Crea un proyecto.
2. Registra una aplicación web.
3. Habilita **Authentication**.
4. En proveedores de inicio de sesión habilita **Email/Password**.
5. Crea **Cloud Firestore**.

### 2. Configuración del SDK web

Completa estas variables con la configuración de la aplicación web:

```
FIREBASE_WEB_API_KEY
FIREBASE_WEB_AUTH_DOMAIN
FIREBASE_WEB_PROJECT_ID
FIREBASE_WEB_STORAGE_BUCKET
FIREBASE_WEB_MESSAGING_SENDER_ID
FIREBASE_WEB_APP_ID
```

Estos valores pertenecen al SDK web. No son equivalentes a las credenciales privadas de la cuenta de servicio.

### 3. Cuenta de servicio para Django

Genera una cuenta de servicio para que el backend pueda utilizar Firebase Admin SDK.

Puedes indicar una ruta:

```
FIREBASE_SERVICE_ACCOUNT_JSON=/ruta/segura/service-account.json
```

o utilizar una versión Base64:

```
FIREBASE_SERVICE_ACCOUNT_B64=<JSON-codificado-en-Base64>
```

**Nunca subas el JSON de la cuenta de servicio a GitHub.**

### 4. ID del proyecto

Configura:

```
FIREBASE_PROJECT_ID=tu-proyecto
```

Debe corresponder al proyecto utilizado por Authentication y Firestore.

### 5. Reglas de Firestore

El archivo `firebase.rules` controla el acceso a las colecciones:

- `usuarios/{uid}`: el usuario autenticado solo puede acceder a su propio perfil.
- `simulaciones/{id}`: un estudiante solo puede leer sus propias simulaciones.
- Los roles `docente` y `admin` pueden leer simulaciones de estudiantes.
- Un estudiante no puede crear una simulación asignándola a otro usuario.
- Un estudiante no puede modificar ni eliminar simulaciones ajenas.

Aplica las reglas mediante Firebase CLI o la herramienta de reglas disponible en tu proyecto.

## Ejemplo de variables

```text
DJANGO_SECRET_KEY=clave-segura
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
TIME_ZONE=America/Santiago

FIREBASE_ENABLED=True
FIREBASE_PROJECT_ID=mi-proyecto

FIREBASE_SERVICE_ACCOUNT_JSON=/ruta/segura/service-account.json
FIREBASE_SERVICE_ACCOUNT_B64=

FIREBASE_WEB_API_KEY=...
FIREBASE_WEB_AUTH_DOMAIN=...
FIREBASE_WEB_PROJECT_ID=mi-proyecto
FIREBASE_WEB_STORAGE_BUCKET=...
FIREBASE_WEB_MESSAGING_SENDER_ID=...
FIREBASE_WEB_APP_ID=...
```

## Uso del sistema

### Registro

1. Entrar a `/registro/`.
2. Ingresar nombre, correo y contraseña.
3. Firebase Authentication crea la cuenta.
4. Django guarda el perfil en Firestore con rol `estudiante`.

### Inicio de sesión

1. Entrar a `/login/`.
2. Ingresar correo y contraseña.
3. Firebase valida las credenciales.
4. Django verifica el ID token.
5. Se crea la sesión del servidor.
6. El usuario ingresa al dashboard.

### Crear una simulación

Desde **Nueva simulación** se configuran:

- Nombre del escenario.
- Virus/enfermedad.
- Tasa de infección.
- Tasa de recuperación.
- Tasa de mortalidad.
- Duración promedio.
- Población.
- Infectados iniciales.
- Duración de la simulación.
- Rango etario.
- Porcentaje estimado de asintomáticos.

Al ejecutar se generan:

- Curvas S/E/I/R/D.
- Día del pico de infectados.
- Máximo de infectados, recuperados y fallecidos.
- Porcentajes respecto de la población.
- Estimación de sintomáticos y asintomáticos.
- Recomendaciones académicas.
- Registro persistente del escenario.

### Comparar

La sección **Comparar** permite seleccionar hasta cuatro simulaciones disponibles para el usuario y contrastar sus indicadores principales.

### Revisión

Un estudiante puede revisar sus propias simulaciones. Los perfiles `docente` y `admin` pueden revisar las simulaciones almacenadas de los estudiantes.

## Roles y permisos

| Rol | Simular | Ver propias | Ver estudiantes | Administración |
|---|---:|---:|---:|---:|
| `estudiante` | Sí | Sí | No | No |
| `docente` | Sí | Sí | Sí | No |
| `admin` | Sí | Sí | Sí | Sí* |

* La administración de usuarios y roles puede realizarse mediante las herramientas administrativas configuradas para el proyecto. La aplicación no entrega una pantalla pública para que un estudiante cambie su propio rol.

El rol se almacena en `usuarios/{uid}.rol` y se utiliza para aplicar las restricciones de acceso.

## Seguridad

Se aplican las siguientes medidas:

- Firebase Authentication para credenciales.
- Verificación server-side del ID token mediante Firebase Admin SDK.
- Sesión de servidor Django después de validar el token.
- Decorador `login_required` para rutas privadas.
- Validación de parámetros epidemiológicos.
- Control de rango etario.
- Validación de infectados iniciales respecto de la población.
- Reglas de Firestore por UID y rol.
- Cuenta de servicio fuera del repositorio.
- `.env` excluido de Git.
- Cookies y encabezados de seguridad cuando `DJANGO_DEBUG=False`.

Para producción utiliza una `DJANGO_SECRET_KEY` segura y configura `DJANGO_ALLOWED_HOSTS` con el dominio real.

## Pruebas

Ejecuta:

```bash
python manage.py test
```

Las pruebas cubren:

- Conservación de la población en el modelo.
- Ausencia de valores negativos.
- Validación de tasas.
- Acceso protegido al simulador.
- Respuesta de la vista de simulación.
- Renderización de resultados.

También puedes verificar la configuración de Django:

```bash
python manage.py check
```

El repositorio incluye una GitHub Action en `.github/workflows/django.yml` para ejecutar automáticamente `check` y `test` en pushes y pull requests.

## Despliegue

El proyecto incluye **Gunicorn** para ejecutarse como aplicación WSGI.

Comando de referencia:

```bash
gunicorn simuladorEcosistema.wsgi:application
```

Variables que deben configurarse en producción:

```text
DJANGO_SECRET_KEY=<valor-seguro>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<dominio>
FIREBASE_ENABLED=True
FIREBASE_PROJECT_ID=<proyecto>
FIREBASE_SERVICE_ACCOUNT_B64=<credencial-segura>
FIREBASE_WEB_API_KEY=<valor>
FIREBASE_WEB_AUTH_DOMAIN=<valor>
FIREBASE_WEB_PROJECT_ID=<valor>
FIREBASE_WEB_STORAGE_BUCKET=<valor>
FIREBASE_WEB_MESSAGING_SENDER_ID=<valor>
FIREBASE_WEB_APP_ID=<valor>
```

No almacenes credenciales privadas de Firebase en el código fuente.

## Limitaciones

- El modelo es una aproximación educativa y no reemplaza modelos epidemiológicos especializados.
- Los parámetros ingresados no representan automáticamente estadísticas oficiales.
- La orientación sanitaria es general y no constituye diagnóstico médico.
- Firestore es NoSQL y no implementa procedimientos almacenados SQL.
- Django utiliza SQLite como soporte interno; la persistencia de simulaciones y perfiles se realiza en Firestore.
- La aplicación requiere Firebase configurado para disponer de autenticación y persistencia en la nube.

## Rúbrica y decisiones técnicas

### Base de datos NoSQL

Se utiliza **Cloud Firestore** porque el proyecto requiere almacenar perfiles y escenarios con estructuras flexibles y acceso por usuario y rol.

### Procedimientos almacenados

Firestore no tiene procedimientos almacenados SQL. Por eso las operaciones de persistencia se encapsulan en `firebase_service.py` y las restricciones de acceso se aplican mediante reglas de Firestore.

No se debe presentar una consulta Firestore como si fuera un procedimiento almacenado SQL.

Si la evaluación exige literalmente un procedimiento almacenado SQL, sería necesario incorporar una base de datos relacional adicional y justificar esa decisión arquitectónica.

### Hardware y software

La solución no requiere hardware físico especializado. El entorno mínimo corresponde a un equipo capaz de ejecutar Python y un navegador. Firebase proporciona la infraestructura cloud para autenticación y almacenamiento.

## Solución de problemas

### "Firebase no está configurado en el servidor"

Verifica:

- `FIREBASE_ENABLED=True`.
- `FIREBASE_PROJECT_ID`.
- Cuenta de servicio válida.
- `FIREBASE_SERVICE_ACCOUNT_JSON` o `FIREBASE_SERVICE_ACCOUNT_B64`.
- Permisos del backend sobre Firestore.

### El login funciona pero no entra al dashboard

Comprueba:

1. Authentication → Email/Password está habilitado.
2. Las variables `FIREBASE_WEB_*` son correctas.
3. El backend puede validar el ID token.
4. La cuenta de servicio pertenece al proyecto indicado.

### Las simulaciones no aparecen

Comprueba:

- Firestore está habilitado.
- Las credenciales del backend son correctas.
- La colección `simulaciones` puede ser consultada por la cuenta de servicio.
- El usuario tiene un UID válido en la sesión.

### El navegador muestra errores de Firebase

Abre las herramientas de desarrollador del navegador y revisa la consola. Los errores del SDK web normalmente indican qué configuración falta o no coincide.

## Estado del proyecto

El proyecto está preparado para desarrollo académico, demostración y pruebas locales. Antes de utilizarlo en producción se deben configurar Firebase, las variables de entorno, el dominio permitido y las medidas de seguridad correspondientes.

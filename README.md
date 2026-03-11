# Simulador de Ecosistema Epidemiológico (SEIRD)

Aplicación web construida con **Django** para simular la evolución de una enfermedad infecciosa en una población.

## ¿Qué hace el programa?

El sistema permite ingresar parámetros epidemiológicos y obtener:

- Curvas de evolución de:
  - Susceptibles (S)
  - Expuestos (E)
  - Infectados (I)
  - Recuperados (R)
  - Fallecidos (D)
- Métricas clave:
  - Día del pico de contagio
  - % máximo de infectados
  - % máximo de recuperados
- Recomendaciones automáticas según el comportamiento de la simulación.

## Modelo utilizado

Se usa una aproximación discreta del modelo **SEIRD**, donde cada día se calculan:

1. Nuevos expuestos por contacto entre susceptibles e infectados.
2. Nuevos infectados a partir del grupo expuesto (incubación).
3. Nuevos recuperados desde infectados.
4. Nuevos fallecidos desde infectados remanentes.

## Requisitos

- Python 3.10+
- pip

## Instalación

Desde la raíz del repo:

```bash
cd simuladorEcosistema
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install django matplotlib numpy
```

## Ejecución

```bash
cd simuladorEcosistema
python manage.py migrate
python manage.py runserver
```

Luego abre: `http://127.0.0.1:8000/`

## Configuración de base de datos

Por defecto usa **SQLite** para funcionar sin configuración extra.

Si quieres usar MySQL, define:

- `USE_MYSQL=True`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`

## Pruebas

```bash
cd simuladorEcosistema
python manage.py test
```

## Estructura principal

- `simuladorEcosistema/simuladorApp/views.py`: lógica de formularios, simulación y render de resultados.
- `simuladorEcosistema/simuladorApp/utilis.py`: motor de simulación SEIRD.
- `simuladorEcosistema/simuladorApp/forms.py`: validaciones de negocio.
- `simuladorEcosistema/templates/simuladorApp/`: pantallas HTML.

## Mejoras aplicadas

- Corrección del algoritmo epidemiológico para que evolucione de forma coherente.
- Validaciones robustas de entrada (rangos, consistencia de población).
- Configuración de entorno más profesional (variables y fallback SQLite).
- Pruebas automatizadas de modelo, formulario y vista.

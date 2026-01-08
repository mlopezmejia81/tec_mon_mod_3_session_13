# Iris ML Classification Pipeline

Proyecto completo de Machine Learning para clasificación de especies de Iris implementando todas las mejores prácticas de desarrollo en Python.

## 📋 Características

Este proyecto incluye:

- **PEP 8 y pycodestyle**: Código siguiendo estándares de Python
- **Python Annotations**: Type hints completos en todo el código
- **Docstrings**: Documentación completa usando Google style
- **PEP 621**: Metadatos del proyecto en `pyproject.toml`
- **Poetry**: Gestión de dependencias moderna
- **Dynaconf**: Configuración por entornos
- **Pruebas completas**:
  - Pruebas unitarias
  - Pruebas de integración
  - Pruebas funcionales
- **Pytest**: Framework de testing con cobertura
- **GitHub Actions**: CI/CD automatizado
- **Refactorización y buenas prácticas**: Código limpio y mantenible
- **POO**: Programación orientada a objetos
- **REST API**: API REST con FastAPI
- **Pydantic**: Validación de datos
- **Pipelines scikit-learn**: `BaseEstimator` y `TransformerMixin`

## 🚀 Instalación

### Requisitos previos

- Python 3.9 o superior
- Poetry

### Instalación con Poetry (Recomendado)

```bash
# Instalar Poetry si no lo tienes
# Si tienes problemas con SSL, usa: pip install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependencias (esto crea el entorno virtual automáticamente)
poetry install

# Activar el entorno virtual (Poetry 2.0+)
# Opción 1: Usar poetry env activate (recomendado)
poetry env activate

# Opción 2: Activar manualmente
source .venv/bin/activate  # En macOS/Linux
# .venv\Scripts\activate   # En Windows

# Opción 3: Instalar el plugin shell para usar 'poetry shell'
poetry self add poetry-plugin-shell
# Luego usar: poetry shell
```

### Instalación alternativa (pip)

Si Poetry no funciona o prefieres usar pip directamente:

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias principales
pip install -r requirements.txt

# Instalar dependencias de desarrollo (opcional)
pip install -r requirements-dev.txt

# Instalar el paquete en modo desarrollo
pip install -e .
```

> **Nota**: Si tienes problemas con la instalación de Poetry debido a certificados SSL, consulta [INSTALL.md](INSTALL.md) para métodos alternativos.

## 📊 Dataset

El proyecto usa el dataset clásico de Iris (`Iris.csv`) que contiene:
- 150 muestras
- 4 características: sepal length, sepal width, petal length, petal width
- 3 clases: Iris-setosa, Iris-versicolor, Iris-virginica

## 🏗️ Estructura del Proyecto

```
tec_mon_mod_3_session_13/
├── src/
│   └── iris_ml/
│       ├── __init__.py
│       ├── api/                 # API REST con FastAPI
│       │   ├── __init__.py
│       │   ├── main.py
│       │   └── schemas.py
│       ├── config/              # Configuración con Dynaconf
│       │   ├── __init__.py
│       │   └── settings.py
│       ├── models/              # Modelos de ML
│       │   ├── __init__.py
│       │   └── pipeline.py
│       ├── preprocessing/       # Transformers personalizados
│       │   ├── __init__.py
│       │   └── transformers.py
│       ├── utils/               # Utilidades
│       │   ├── __init__.py
│       │   └── data_loader.py
│       ├── train.py             # Script de entrenamiento
│       └── predict.py           # Script de predicción
├── tests/
│   ├── unit/                    # Pruebas unitarias
│   ├── integration/             # Pruebas de integración
│   └── functional/              # Pruebas funcionales
├── docs/                        # Documentación
├── .github/
│   └── workflows/               # GitHub Actions
├── pyproject.toml               # Configuración Poetry y PEP 621
├── settings.toml                # Configuración Dynaconf
└── README.md
```

## 🔧 Uso

### Entrenar el modelo

```bash
# Con Poetry
poetry run iris-train

# O directamente
python -m iris_ml.train
```

### Realizar predicciones (CLI)

```bash
# Con Poetry
poetry run iris-predict

# O directamente
python -m iris_ml.predict
```

### Iniciar la API REST

```bash
# Con Poetry
poetry run iris-api

# O directamente
python -m iris_ml.api.main

# O con uvicorn
uvicorn iris_ml.api.main:app --reload
```

La API estará disponible en `http://localhost:8000`

### Documentación de la API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Ejemplo de uso de la API

```bash
# Health check
curl http://localhost:8000/health

# Predicción individual
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "features": {
         "sepal_length_cm": 5.1,
         "sepal_width_cm": 3.5,
         "petal_length_cm": 1.4,
         "petal_width_cm": 0.2
       }
     }'
```

## 🧪 Testing

### Ejecutar todas las pruebas

```bash
poetry run pytest
```

### Ejecutar pruebas por categoría

```bash
# Pruebas unitarias
poetry run pytest tests/unit/

# Pruebas de integración
poetry run pytest tests/integration/

# Pruebas funcionales
poetry run pytest tests/functional/
```

### Con cobertura

```bash
poetry run pytest --cov=src/iris_ml --cov-report=html
```

El reporte de cobertura estará en `htmlcov/index.html`

## 🔍 Linting y Code Quality

### Pycodestyle (PEP 8)

```bash
poetry run pycodestyle src/ tests/
```

### Pydocstyle (docstrings)

```bash
poetry run pydocstyle src/
```

### Black (formateo)

```bash
# Verificar
poetry run black --check src/ tests/

# Formatear
poetry run black src/ tests/
```

### MyPy (type checking)

```bash
poetry run mypy src/
```

## ⚙️ Configuración

La configuración se maneja con Dynaconf usando múltiples fuentes:

### 1. Variables de Entorno (`.env`) - Para credenciales y secretos

Crea un archivo `.env` en la raíz del proyecto basado en `env.example`:

```bash
# Copiar el archivo de ejemplo
cp env.example .env

# Editar .env con tus valores reales
nano .env  # o usa tu editor favorito
```

El archivo `.env` contiene variables sensibles que NO deben versionarse:
- `SECRET_KEY`: Clave secreta de la aplicación
- `API_KEY`, `API_SECRET`: Credenciales de APIs externas
- `DB_PASSWORD`: Contraseñas de base de datos
- `ENV_FOR_DYNACONF`: Entorno actual (development, testing, production)

### 2. Archivo de Configuración (`config.yml`) - Para configuración general

El archivo `config.yml` contiene configuración estructurada por entornos:

```yaml
default: &default
  debug: false
  log_level: "INFO"
  data_path: "Iris.csv"
  model_path: "models/iris_model.pkl"
  ml:
    n_estimators: 100
  api:
    host: "0.0.0.0"
    port: 8000

development: &development
  <<: *default
  debug: true
  log_level: "DEBUG"
```

### 3. Prioridad de Configuración

Dynaconf lee la configuración en este orden (mayor prioridad primero):

1. **Variables de entorno del sistema** (variables exportadas)
2. **Archivo `.env`** (variables de entorno locales)
3. **`config.yml`** (configuración por entorno)
4. **`settings.toml`** (configuración alternativa, mantiene compatibilidad)

### 4. Cambiar Entorno

Usa la variable de entorno `ENV_FOR_DYNACONF`:

```bash
# En .env
ENV_FOR_DYNACONF=production

# O exportar directamente
export ENV_FOR_DYNACONF=production
poetry run iris-api
```

### 5. Acceder a la Configuración en Código

```python
from iris_ml.config import settings

# Configuración básica
debug = settings.debug
log_level = settings.log_level

# Configuración anidada (desde config.yml)
n_estimators = settings.ml.n_estimators
api_port = settings.api.port

# Variables de entorno (desde .env)
secret_key = settings.secret_key
api_key = settings.api_key
```

### 6. Ejemplo de Uso

```python
# En .env
ENV_FOR_DYNACONF=development
SECRET_KEY=mi-clave-secreta
DEBUG=true

# En config.yml
development:
  api:
    port: 8000

# El código usará:
# - DEBUG=true (de .env)
# - api.port=8000 (de config.yml)
# - ENV_FOR_DYNACONF=development (de .env)
```

## 📚 Documentación del Código

El proyecto sigue el estilo Google para docstrings:

```python
def ejemplo_funcion(param1: int, param2: str) -> bool:
    """Descripción breve de la función.

    Descripción más detallada si es necesario.

    Args:
        param1: Descripción del primer parámetro.
        param2: Descripción del segundo parámetro.

    Returns:
        Descripción del valor de retorno.

    Raises:
        ValueError: Cuando algo sale mal.
    """
    pass
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## 👥 Autores

- Miguel Angel Mejia

## 🙏 Agradecimientos

- Scikit-learn por las herramientas de ML
- FastAPI por el framework de API
- Poetry por la gestión de dependencias
- Y todos los demás proyectos open source que hacen esto posible

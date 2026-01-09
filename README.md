# Iris ML Classification Pipeline

Proyecto completo de Machine Learning para clasificación de especies de Iris implementando todas las mejores prácticas de desarrollo en Python.

## 📋 Características

Este proyecto incluye:

- **PEP 8 y pycodestyle**: Código siguiendo estándares de Python
  - Verificado en: Todos los archivos `.py` en `src/` y `tests/`
  - Configuración: `pyproject.toml` (sección `[tool.pycodestyle]`)
  - Verificación automática: `.github/workflows/ci.yml` (job `lint`)

- **Python Annotations**: Type hints completos en todo el código
  - Implementado en: Todos los archivos `.py` del proyecto
  - Ejemplos destacados: `src/iris_ml/models/pipeline.py`, `src/iris_ml/api/main.py`, `src/iris_ml/utils/data_loader.py`

- **Docstrings**: Documentación completa usando Google style
  - Implementado en: Todos los módulos y funciones del proyecto
  - Verificado con: `pydocstyle` (configurado en `pyproject.toml`)
  - Ejemplos: `src/iris_ml/models/pipeline.py`, `src/iris_ml/api/schemas.py`

- **PEP 621**: Metadatos del proyecto en `pyproject.toml`
  - Archivo: `pyproject.toml` (sección `[tool.poetry]`)
  - Incluye: nombre, versión, descripción, autores, dependencias

- **Poetry**: Gestión de dependencias moderna
  - Archivos: `pyproject.toml`, `poetry.lock`
  - Scripts definidos: `pyproject.toml` (sección `[tool.poetry.scripts]`)
  - Comandos: `iris-train`, `iris-predict`, `iris-api`

- **Dynaconf**: Configuración por entornos
  - Archivos de configuración: `config.yml`, `.env`, `settings.toml`
  - Implementación: `src/iris_ml/config/settings.py`
  - Ejemplo de uso: `src/iris_ml/models/pipeline.py`, `src/iris_ml/api/main.py`

- **Pruebas completas**:
  - Pruebas unitarias: `tests/unit/` (ej: `test_pipeline.py`, `test_transformers.py`, `test_data_loader.py`)
  - Pruebas de integración: `tests/integration/` (ej: `test_training_pipeline.py`)
  - Pruebas funcionales: `tests/functional/` (ej: `test_api.py`)
  - Fixtures compartidas: `tests/conftest.py`

- **Pytest**: Framework de testing con cobertura
  - Configuración: `pyproject.toml` (sección `[tool.pytest.ini_options]`)
  - Reportes: Generados en `htmlcov/` después de ejecutar tests con `--cov`
  - CI/CD: `.github/workflows/ci.yml` (job `test`)

- **GitHub Actions**: CI/CD automatizado
  - Archivo: `.github/workflows/ci.yml`
  - Jobs: `lint` (calidad de código), `test` (pruebas), `build` (construcción del paquete)

- **Refactorización y buenas prácticas**: Código limpio y mantenible
  - Implementado en: Todo el código del proyecto
  - Ejemplos: `src/iris_ml/utils/column_cleaner.py` (función genérica para limpieza de columnas)

- **POO**: Programación orientada a objetos
  - Clases principales: `src/iris_ml/models/pipeline.py` (`IrisPipeline`)
  - Transformers personalizados: `src/iris_ml/preprocessing/transformers.py` (`ColumnSelector`, `SpeciesEncoder`)

- **REST API**: API REST con FastAPI
  - Archivo principal: `src/iris_ml/api/main.py`
  - Endpoints: `/`, `/health`, `/predict`
  - Documentación automática: Swagger UI (`/docs`) y ReDoc (`/redoc`)

- **Pydantic**: Validación de datos
  - Archivo: `src/iris_ml/api/schemas.py`
  - Modelos: `IrisFeatures`, `PredictionRequest`, `PredictionResponse`, `HealthResponse`

- **Pipelines scikit-learn**: `BaseEstimator` y `TransformerMixin`
  - Transformers personalizados: `src/iris_ml/preprocessing/transformers.py`
    - `ColumnSelector`: Hereda de `BaseEstimator` y `TransformerMixin`
    - `SpeciesEncoder`: Hereda de `BaseEstimator` y `TransformerMixin`
  - Pipeline completo: `src/iris_ml/models/pipeline.py` (`IrisPipeline`)

## 🚀 Instalación

### Requisitos previos

- Python 3.9 o superior
- Poetry

### Instalación con Poetry (Recomendado)

#### Paso 1: Instalar Poetry

**⚠️ Importante**: Poetry debe instalarse **fuera** de un entorno virtual para que esté disponible globalmente.

```bash
# Opción 1: Instalación oficial (si NO tienes problemas de SSL)
# Esto instala Poetry en ~/.local/bin (Linux/macOS) o %APPDATA%\Python\Scripts (Windows)
curl -sSL https://install.python-poetry.org | python3 -

# Después de instalar, agrega Poetry al PATH (macOS/Linux)
# Agrega esta línea a tu ~/.zshrc o ~/.bashrc:
export PATH="$HOME/.local/bin:$PATH"
source ~/.zshrc  # o source ~/.bashrc

# Opción 2: Si tienes problemas de SSL (CERTIFICATE_VERIFY_FAILED) - RECOMENDADO EN macOS
# Usa pip directamente (funciona incluso con problemas de certificados):
python3 -m pip install --user poetry

# Después de instalar, agrega Poetry al PATH (para Python 3.13 en macOS):
# Reemplaza 3.13 con tu versión de Python si es diferente:
export PATH="$HOME/Library/Python/3.13/bin:$PATH"

# Agrega esta línea a tu ~/.zshrc para que persista:
echo 'export PATH="$HOME/Library/Python/3.13/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verifica la instalación:
poetry --version

# Opción 3: Usar pipx (si lo tienes instalado - requiere certificados SSL funcionando)
pipx install poetry
```

**Si ya instalaste Poetry dentro de un venv** (temporal para instalarlo):
```bash
# El venv donde instalaste Poetry es solo temporal
# Una vez que Poetry esté instalado globalmente, puedes eliminarlo
# Para usar Poetry mientras tanto:
source venv/bin/activate  # Activa el venv donde está Poetry
poetry install  # Poetry creará su PROPIO entorno virtual para el proyecto
```

**⚠️ Problema común: Poetry funciona en terminal normal pero no en Cursor/VS Code**

**Problema**: Cursor y VS Code ejecutan shells no interactivos que no cargan `.zshrc` automáticamente.

**Solución**:
```bash
# Agregar el PATH a .zprofile (se carga siempre, incluso en shells no interactivos)
echo 'export PATH="$HOME/Library/Python/3.13/bin:$PATH"' >> ~/.zprofile

# También puedes agregarlo a .zshenv para máxima compatibilidad
echo 'export PATH="$HOME/Library/Python/3.13/bin:$PATH"' >> ~/.zshenv

# Cierra y reabre Cursor/VS Code para que los cambios surtan efecto
# O en una terminal nueva dentro de Cursor, ejecuta:
source ~/.zprofile
```

**Verificación rápida en Cursor**:
```bash
# En la terminal de Cursor, ejecuta temporalmente:
export PATH="$HOME/Library/Python/3.13/bin:$PATH"
poetry --version  # Debería funcionar ahora

# Para que persista, asegúrate de tenerlo en .zprofile
```

#### Paso 2: Instalar dependencias del proyecto

```bash
# Instalar dependencias (esto crea el entorno virtual automáticamente)
poetry install

# Poetry creará un entorno virtual SEPARADO para este proyecto
# No necesitas activar el venv temporal donde instalaste Poetry
```

#### Paso 3: Activar el entorno virtual del proyecto

**Opción 1: Usar `poetry env activate` (recomendado por Poetry)**
```bash
poetry env activate
```

**Opción 2: Activar manualmente**
```bash
source .venv/bin/activate
# o
source $(poetry env info --path)/bin/activate
deactivate
```

**Opción 3: Usar `poetry shell`**
```bash
poetry self add poetry-plugin-shell
poetry shell
exit
```

**Opción 4: Usar `poetry run` (sin activar)**
```bash
poetry run pytest
poetry run iris-train
poetry run iris-api
```

**📝 Resumen importante**:

- ✅ Poetry debe estar instalado **globalmente** (fuera de venvs) para uso normal
- ✅ El venv donde instalaste Poetry (si usaste uno) es **temporal** y solo sirve para tener Poetry disponible
- ✅ Poetry crea su **propio entorno virtual** para cada proyecto cuando ejecutas `poetry install` (separado del venv temporal)
- ✅ Para activar el entorno virtual del proyecto, usa una de las 3 opciones mostradas arriba
- ✅ **Importante**: El comando `poetry env activate` **NO EXISTE** (es un error común de documentación)

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

### Ver el reporte de cobertura

El reporte de cobertura se genera en formato HTML y puedes verlo de las siguientes formas:

#### 1. Localmente (después de ejecutar los tests)

Después de ejecutar los tests con cobertura, el reporte se genera en la carpeta `htmlcov/`:

```bash
# Generar el reporte
poetry run pytest --cov=src/iris_ml --cov-report=html

# Abrir el reporte en tu navegador
# En macOS:
open htmlcov/index.html

# En Linux:
xdg-open htmlcov/index.html

# En Windows:
start htmlcov/index.html
```

El reporte HTML muestra:
- Porcentaje de cobertura por archivo
- Líneas cubiertas y no cubiertas (resaltadas en color)
- Resumen general del proyecto

#### 2. En GitHub Actions (después de que el workflow se ejecute)

1. Ve a la pestaña **"Actions"** en tu repositorio de GitHub
2. Abre la ejecución del workflow que quieras revisar
3. Al final de la página, en la sección **"Artifacts"**, verás **"coverage-html"**
4. Descarga el artifact y abre `htmlcov/index.html` en tu navegador

> **Nota**: Los artifacts se mantienen disponibles por 30 días después de la ejecución del workflow.

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

---

## 📦 Instalación Adicional: Paquete Distribuible

### Instalar el paquete distribuible (desde archivos generados)

Si has construido el paquete con `poetry build`, puedes instalar los archivos generados en la carpeta `dist/`:

#### Construir el paquete

```bash
poetry build
```

Esto crea dos archivos en la carpeta `dist/`:
- `iris_ml_pipeline-0.1.0-py3-none-any.whl` (wheel - recomendado)
- `iris-ml-pipeline-0.1.0.tar.gz` (source distribution)

#### Instalar desde el archivo .whl (recomendado)

```bash
pip install dist/iris_ml_pipeline-0.1.0-py3-none-any.whl
# o con Poetry
poetry run pip install dist/iris_ml_pipeline-0.1.0-py3-none-any.whl
```

#### Instalar desde el archivo .tar.gz

```bash
pip install dist/iris-ml-pipeline-0.1.0.tar.gz
```

#### Instalar desde la carpeta dist/ completa

```bash
pip install dist/
```

#### Verificar la instalación

```bash
pip show iris-ml-pipeline
iris-train --help
iris-predict --help
iris-api --help
```

#### Desinstalar

```bash
pip uninstall iris-ml-pipeline
```

---

## 🔧 Solución de Problemas Comunes

### Error: `[SSL: CERTIFICATE_VERIFY_FAILED]` al instalar Poetry

**Problema**: Los certificados SSL de Python no están configurados correctamente en macOS.

**Solución rápida**:
```bash
python3 -m pip install --user poetry
export PATH="$HOME/Library/Python/3.13/bin:$PATH"
echo 'export PATH="$HOME/Library/Python/3.13/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
poetry --version
```

**Solución alternativa**:
```bash
/Applications/Python\ 3.13/Install\ Certificates.command
curl -sSL https://install.python-poetry.org | python3 -
```

### Error: `command not found: poetry`

**Problema**: Poetry no está disponible en tu PATH.

**Solución**:

1. **Si instalaste Poetry con el script oficial**:
   ```bash
   ls -la ~/.local/bin/poetry
   # o
   ls -la ~/Library/Python/*/bin/poetry
   export PATH="$HOME/.local/bin:$PATH"
   # o para macOS
   export PATH="$HOME/Library/Python/3.x/bin:$PATH"
   source ~/.zshrc
   ```

2. **Si instalaste Poetry dentro de un venv (temporal)**:
   ```bash
   source venv/bin/activate
   poetry install
   # Una vez instalado globalmente:
   deactivate
   rm -rf venv
   ```

3. **Reinstalar Poetry correctamente**:
   ```bash
   # Opción A: Con pip (recomendado si hay problemas de SSL)
   python3 -m pip install --user poetry
   export PATH="$HOME/Library/Python/3.13/bin:$PATH"
   echo 'export PATH="$HOME/Library/Python/3.13/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   
   # Opción B: Script oficial (si no hay problemas de SSL)
   curl -sSL https://install.python-poetry.org | python3 -
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   
   # Opción C: Con pipx
   python3 -m pip install --user pipx
   python3 -m pipx ensurepath
   pipx install poetry
   ```

### ¿Por qué necesito activar un venv para usar Poetry si Poetry crea su propio venv?

**Explicación**:
- Si instalaste Poetry dentro de un venv, ese venv es solo temporal para tener Poetry disponible
- Cuando ejecutas `poetry install`, Poetry crea su propio entorno virtual separado para el proyecto
- **Opciones**:
  1. **Temporal**: Mantener el venv donde está Poetry activo solo para comandos Poetry
  2. **Permanente**: Instalar Poetry globalmente (recomendado)

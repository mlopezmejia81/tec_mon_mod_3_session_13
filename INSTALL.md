# Guía de Instalación

## Opción 1: Usando Poetry (Recomendado)

### Instalación de Poetry

Si tienes problemas con SSL al instalar Poetry (como el error que viste), puedes usar estos métodos alternativos:

#### Método A: Instalación directa sin SSL

```bash
# Opción 1: Usar pipx (si está disponible)
pipx install poetry

# Opción 2: Instalar desde pip
pip install poetry

# Opción 3: Instalar Poetry manualmente
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - --version 1.7.1
```

#### Método B: Usar pip directamente (alternativa)

Si Poetry no funciona, puedes instalar las dependencias directamente con pip:

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias principales
pip install -r requirements.txt

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Instalar el paquete en modo desarrollo
pip install -e .
```

### Uso con Poetry

```bash
# Instalar dependencias
poetry install

# Activar entorno virtual
poetry shell

# Ejecutar comandos
poetry run pytest
poetry run iris-train
```

## Opción 2: Usando pip (Alternativa)

### Instalación paso a paso

```bash
# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar entorno virtual
source venv/bin/activate  # En macOS/Linux
# O en Windows:
# venv\Scripts\activate

# 3. Actualizar pip
pip install --upgrade pip

# 4. Instalar dependencias principales
pip install -r requirements.txt

# 5. Instalar dependencias de desarrollo (opcional)
pip install -r requirements-dev.txt

# 6. Instalar el paquete en modo desarrollo
pip install -e .
```

## Verificación de Instalación

Después de instalar, verifica que todo funciona:

```bash
# Verificar que el paquete está instalado
python -c "import iris_ml; print(iris_ml.__version__)"

# Verificar imports principales
python -c "from iris_ml.models import IrisPipeline; print('OK')"
python -c "from iris_ml.api import app; print('OK')"

# Ejecutar pruebas
pytest tests/unit/ -v
```

## Solución de Problemas

### Error: Certificate verify failed

Si tienes problemas con certificados SSL (como en la instalación de Poetry):

```bash
# Opción 1: Actualizar certificados en macOS
# Descargar e instalar desde: https://www.python.org/downloads/
# O ejecutar:
/Applications/Python\ 3.x/Install\ Certificates.command

# Opción 2: Usar pip directamente en lugar de Poetry
pip install -r requirements.txt -r requirements-dev.txt
```

### Error: Module not found

Si hay módulos faltantes:

```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Reinstalar todo
pip install --force-reinstall -r requirements.txt -r requirements-dev.txt
pip install -e .
```

### Error: Permission denied

```bash
# No uses sudo con venv
# Si necesitas permisos, recrea el venv
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Dependencias Principales

Las siguientes son las dependencias principales del proyecto:

### Core Dependencies

- **scikit-learn**: Machine Learning
- **fastapi**: Framework web para API REST
- **uvicorn**: Servidor ASGI
- **pydantic**: Validación de datos
- **pandas**: Manipulación de datos
- **numpy**: Computación numérica
- **dynaconf**: Configuración por entornos
- **httpx**: Cliente HTTP (para tests)

### Development Dependencies

- **pytest**: Framework de testing
- **pytest-cov**: Cobertura de código
- **black**: Formateo de código
- **pycodestyle**: Verificación PEP 8
- **pydocstyle**: Verificación de docstrings
- **mypy**: Verificación de tipos
- **ruff**: Linter rápido

## Comandos Útiles

```bash
# Actualizar dependencias
poetry update  # Con Poetry
pip install --upgrade -r requirements.txt  # Con pip

# Ver dependencias instaladas
poetry show  # Con Poetry
pip list  # Con pip

# Verificar dependencias
poetry check  # Con Poetry
pip check  # Con pip
```

## Notas

- Python 3.9 o superior es requerido
- Se recomienda usar un entorno virtual siempre
- Poetry es opcional pero recomendado para gestión de dependencias
- Si Poetry no funciona, pip + requirements.txt funciona perfectamente

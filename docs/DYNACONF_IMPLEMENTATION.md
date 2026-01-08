# Implementación de Dynaconf - Guía Práctica

## ¿Qué es Dynaconf?

Dynaconf es una biblioteca que permite gestionar configuración desde múltiples fuentes de forma unificada.

## Implementación en el Proyecto

### Archivo Principal: `src/iris_ml/config/settings.py`

```python
from pathlib import Path
from dynaconf import Dynaconf

# Ruta del directorio raíz
ROOT_DIR = Path(__file__).parent.parent.parent.parent

# Configuración de Dynaconf
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        str(ROOT_DIR / "config.yml"),      # Configuración principal
        str(ROOT_DIR / "settings.toml"),   # Configuración alternativa
    ],
    environments=True,                      # Habilitar entornos
    default_env="development",            # Entorno por defecto
    load_dotenv=True,                      # Cargar .env automáticamente
    dotenv_path=str(ROOT_DIR / ".env"),   # Ruta al archivo .env
    env_switcher="ENV_FOR_DYNACONF",      # Variable para cambiar entorno
)
```

## Uso en el Código

### Importar configuración

```python
from iris_ml.config import settings
```

### Acceder a valores

```python
# Valores simples
debug = settings.debug
log_level = settings.log_level

# Valores anidados (desde config.yml)
n_estimators = settings.ml.n_estimators
api_port = settings.api.port

# Variables de entorno (desde .env)
secret_key = settings.secret_key
api_key = settings.api_key
```

## Prioridad de Configuración

1. **Variables de entorno del sistema** (mayor prioridad)
2. **Archivo `.env`**
3. **`config.yml`** (según entorno)
4. **`settings.toml`** (según entorno)

## Cambiar Entorno

```bash
# En .env
ENV_FOR_DYNACONF=production

# O exportar
export ENV_FOR_DYNACONF=production
```

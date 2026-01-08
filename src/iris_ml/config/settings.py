"""Configuración del proyecto usando Dynaconf."""

from pathlib import Path
from typing import Any

from dynaconf import Dynaconf

# Obtener la ruta del directorio raíz del proyecto
ROOT_DIR: Path = Path(__file__).parent.parent.parent.parent

# Configuración de Dynaconf
# Lee configuración de múltiples fuentes en orden de prioridad:
# 1. Variables de entorno (.env)
# 2. config.yml (por entorno)
# 3. settings.toml (por entorno) - mantiene compatibilidad
settings: Dynaconf = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        str(ROOT_DIR / "config.yml"),  # Configuración principal en YAML
        str(ROOT_DIR / "settings.toml"),  # Configuración alternativa en TOML
    ],
    environments=True,
    default_env="development",
    load_dotenv=True,
    dotenv_path=str(ROOT_DIR / ".env"),  # Variables de entorno desde .env
    env_switcher="ENV_FOR_DYNACONF",  # Variable de entorno para cambiar entorno
)

# Atributos de configuración con tipo
def get_data_path() -> Path:
    """Obtiene la ruta del archivo de datos.

    Returns:
        Path: Ruta al archivo CSV de datos.
    """
    return ROOT_DIR / settings.data_path


def get_model_path() -> Path:
    """Obtiene la ruta donde se guardará el modelo.

    Returns:
        Path: Ruta al archivo del modelo entrenado.
    """
    model_dir: Path = ROOT_DIR / settings.model_path
    model_dir.parent.mkdir(parents=True, exist_ok=True)
    return model_dir


def get_config() -> dict[str, Any]:
    """Obtiene la configuración completa como diccionario.

    Returns:
        dict: Configuración completa del proyecto.
    """
    return {
        "debug": settings.debug,
        "log_level": settings.log_level,
        "data_path": get_data_path(),
        "model_path": get_model_path(),
        "test_size": settings.test_size,
        "random_state": settings.random_state,
    }

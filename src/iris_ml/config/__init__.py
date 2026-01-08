"""Módulo de configuración usando Dynaconf."""

from .settings import get_config, get_data_path, get_model_path, settings

__all__ = ["settings", "get_data_path", "get_model_path", "get_config"]

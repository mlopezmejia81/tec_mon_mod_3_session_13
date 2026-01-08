"""Utilidades para limpiar y normalizar nombres de columnas."""

import re
from typing import Any

import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza los nombres de columnas a snake_case.

    Convierte nombres de columnas de cualquier formato (PascalCase, camelCase,
    UPPER_CASE, etc.) a snake_case estándar, manejando números y caracteres especiales.

    Args:
        df: DataFrame con columnas a limpiar.

    Returns:
        DataFrame con nombres de columnas normalizados a snake_case.

    Examples:
        >>> df = pd.DataFrame(columns=["SepalLengthCm", "PetalWidth2", "Id"])
        >>> df_cleaned = clean_column_names(df)
        >>> print(df_cleaned.columns)
        Index(['sepal_length_cm', 'petal_width_2', 'id'], dtype='object')
    """
    df = df.copy()

    # Limpiar espacios en blanco
    df.columns = df.columns.str.strip()

    # Convertir cada nombre de columna
    cleaned_columns = []
    for col in df.columns:
        cleaned_col = _to_snake_case(col)
        cleaned_columns.append(cleaned_col)

    df.columns = cleaned_columns

    return df


def _to_snake_case(name: str) -> str:
    """Convierte un nombre a snake_case.

    Maneja:
    - PascalCase -> snake_case
    - camelCase -> snake_case
    - UPPER_CASE -> snake_case
    - Números preservados
    - Caracteres especiales removidos o reemplazados

    Args:
        name: Nombre a convertir.

    Returns:
        Nombre en formato snake_case.

    Examples:
        >>> _to_snake_case("SepalLengthCm")
        'sepal_length_cm'
        >>> _to_snake_case("petalWidth2")
        'petal_width_2'
        >>> _to_snake_case("ID_NUMBER")
        'id_number'
    """
    if not name:
        return ""

    # Limpiar espacios
    name = name.strip()

    # Si ya está en snake_case y minúsculas, retornar
    if "_" in name and name.islower() and not re.search(r"[A-Z]", name):
        return name

    # Paso 1: Insertar guión bajo antes de mayúsculas que siguen a minúsculas o números
    # "camelCase" -> "camel_Case", "Width2" -> "Width_2"
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)

    # Paso 2: Reemplazar espacios, guiones y otros separadores comunes con guiones bajos
    # Esto debe hacerse ANTES de eliminar caracteres especiales para preservar estructura
    name = re.sub(r"[\s\-\.]+", "_", name)

    # Paso 3: Insertar guión bajo antes de números que siguen a letras
    # "Width2" -> "Width_2", "Petal@Width#2" -> "Petal@Width_#2" (después se limpia)
    # Maneja caracteres especiales opcionales entre letras y números
    name = re.sub(r"([a-zA-Z])[^a-zA-Z0-9]*([0-9])", r"\1_\2", name)

    # Paso 4: Insertar guión bajo después de números que preceden a letras
    # "2Width" -> "2_Width", "2#Width" -> "2_Width"
    # Maneja caracteres especiales opcionales entre números y letras
    name = re.sub(r"([0-9])[^a-zA-Z0-9]*([a-zA-Z])", r"\1_\2", name)

    # Paso 5: Remover caracteres especiales (mantener letras, números y guiones bajos)
    # Esto se hace DESPUÉS de procesar números para preservar la estructura
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)

    # Paso 6: Convertir a minúsculas
    name = name.lower()

    # Paso 7: Remover guiones bajos múltiples
    name = re.sub(r"_+", "_", name)

    # Paso 8: Remover guiones bajos al inicio y final
    name = name.strip("_")

    return name

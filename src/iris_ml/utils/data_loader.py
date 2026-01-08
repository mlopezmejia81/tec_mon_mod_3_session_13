"""Utilidades para cargar y procesar datos."""

from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from iris_ml.config import settings
from iris_ml.config.settings import get_data_path
from iris_ml.utils.column_cleaner import clean_column_names


def load_iris_data(data_path: Path | None = None) -> pd.DataFrame:
    """Carga el dataset de Iris desde un archivo CSV.

    Args:
        data_path: Ruta al archivo CSV. Si es None, usa la configuración.

    Returns:
        DataFrame con los datos de Iris.

    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    if data_path is None:
        data_path = get_data_path()

    if not data_path.exists():
        raise FileNotFoundError(f"El archivo {data_path} no existe.")

    df: pd.DataFrame = pd.read_csv(data_path)

    # Limpiar y normalizar nombres de columnas automáticamente
    # Convierte PascalCase, camelCase, etc. a snake_case
    df = clean_column_names(df)

    return df


def prepare_data(
    test_size: float | None = None, random_state: int | None = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Prepara los datos para entrenamiento y prueba.

    Args:
        test_size: Proporción del dataset para prueba.
        random_state: Semilla para reproducibilidad.

    Returns:
        Tupla con (X_train, X_test, y_train, y_test).
    """
    if test_size is None:
        test_size = settings.test_size
    if random_state is None:
        random_state = settings.random_state

    df: pd.DataFrame = load_iris_data()

    # Seleccionar características y etiqueta
    feature_columns: list[str] = [
        "sepal_length_cm",
        "sepal_width_cm",
        "petal_length_cm",
        "petal_width_cm",
    ]

    X: pd.DataFrame = df[feature_columns]
    y: pd.Series = df["species"]

    # Dividir en train y test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return X_train, X_test, y_train, y_test

"""Configuración compartida para pytest."""

import sys
from pathlib import Path

import pandas as pd
import pytest

# Agregar el directorio src al path
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from iris_ml.models import create_pipeline
from iris_ml.preprocessing import ColumnSelector, SpeciesEncoder
from iris_ml.utils.data_loader import prepare_data


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Fixture con datos de ejemplo para pruebas.

    Returns:
        DataFrame con datos de ejemplo.
    """
    return pd.DataFrame(
        {
            "sepal_length_cm": [5.1, 4.9, 7.0],
            "sepal_width_cm": [3.5, 3.0, 3.2],
            "petal_length_cm": [1.4, 1.4, 4.7],
            "petal_width_cm": [0.2, 0.2, 1.4],
        }
    )


@pytest.fixture
def sample_labels() -> pd.Series:
    """Fixture con etiquetas de ejemplo.

    Returns:
        Serie con etiquetas de especies.
    """
    return pd.Series(["Iris-setosa", "Iris-setosa", "Iris-versicolor"])


@pytest.fixture
def iris_data():
    """Fixture con datos completos de Iris.

    Returns:
        Tupla con (X_train, X_test, y_train, y_test).
    """
    return prepare_data(test_size=0.2, random_state=42)


@pytest.fixture
def trained_pipeline(iris_data):
    """Fixture con un pipeline entrenado.

    Args:
        iris_data: Datos de entrenamiento y prueba.

    Returns:
        Pipeline entrenado.
    """
    X_train, _, y_train, _ = iris_data
    pipeline = create_pipeline(n_estimators=10, random_state=42)
    pipeline.fit(X_train, y_train)
    return pipeline

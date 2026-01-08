"""Transformers personalizados para el pipeline de preprocesamiento."""

from typing import Any, List

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class ColumnSelector(BaseEstimator, TransformerMixin):
    """Selector de columnas para el pipeline.

    Selecciona columnas específicas de un DataFrame de pandas.

    Attributes:
        columns: Lista de nombres de columnas a seleccionar.
    """

    def __init__(self, columns: List[str]) -> None:
        """Inicializa el selector de columnas.

        Args:
            columns: Lista de nombres de columnas a seleccionar.
        """
        self.columns: List[str] = columns

    def fit(self, X: pd.DataFrame, y: Any = None) -> "ColumnSelector":
        """Ajusta el transformador (no hace nada en este caso).

        Args:
            X: DataFrame de entrada.
            y: Etiquetas objetivo (opcional).

        Returns:
            self: Instancia del transformador.
        """
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Selecciona las columnas especificadas.

        Args:
            X: DataFrame de entrada.

        Returns:
            DataFrame con solo las columnas seleccionadas.
        """
        return X[self.columns]


class SpeciesEncoder(BaseEstimator, TransformerMixin):
    """Codificador de especies de Iris.

    Convierte nombres de especies a valores numéricos.

    Attributes:
        species_mapping: Diccionario de mapeo de especies a números.
        inverse_mapping: Diccionario inverso para decodificar.
    """

    def __init__(self) -> None:
        """Inicializa el codificador de especies."""
        self.species_mapping: dict[str, int] = {
            "Iris-setosa": 0,
            "Iris-versicolor": 1,
            "Iris-virginica": 2,
        }
        self.inverse_mapping: dict[int, str] = {
            v: k for k, v in self.species_mapping.items()
        }

    def fit(self, X: pd.Series, y: Any = None) -> "SpeciesEncoder":
        """Ajusta el transformador (no hace nada en este caso).

        Args:
            X: Serie de pandas con especies.
            y: Etiquetas objetivo (opcional).

        Returns:
            self: Instancia del transformador.
        """
        return self

    def transform(self, X: pd.Series) -> np.ndarray:
        """Codifica las especies a valores numéricos.

        Args:
            X: Serie de pandas con especies.

        Returns:
            Array numpy con especies codificadas.
        """
        return np.array([self.species_mapping[species] for species in X])

    def inverse_transform(self, X: np.ndarray) -> List[str]:
        """Decodifica valores numéricos a nombres de especies.

        Args:
            X: Array numpy con valores codificados.

        Returns:
            Lista de nombres de especies.
        """
        return [self.inverse_mapping[int(value)] for value in X]

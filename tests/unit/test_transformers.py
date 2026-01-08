"""Pruebas unitarias para los transformers."""

import pandas as pd
import pytest

from iris_ml.preprocessing import ColumnSelector, SpeciesEncoder


class TestColumnSelector:
    """Pruebas para ColumnSelector."""

    def test_init(self) -> None:
        """Prueba la inicialización del selector."""
        selector = ColumnSelector(columns=["col1", "col2"])
        assert selector.columns == ["col1", "col2"]

    def test_fit(self, sample_data: pd.DataFrame) -> None:
        """Prueba el método fit."""
        selector = ColumnSelector(columns=["sepal_length_cm", "sepal_width_cm"])
        result = selector.fit(sample_data)
        assert result is selector  # Debe retornar self

    def test_transform(self, sample_data: pd.DataFrame) -> None:
        """Prueba el método transform."""
        selector = ColumnSelector(columns=["sepal_length_cm", "sepal_width_cm"])
        selector.fit(sample_data)
        result = selector.transform(sample_data)

        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["sepal_length_cm", "sepal_width_cm"]
        assert len(result) == len(sample_data)

    def test_fit_transform(self, sample_data: pd.DataFrame) -> None:
        """Prueba fit_transform."""
        selector = ColumnSelector(columns=["sepal_length_cm"])
        result = selector.fit_transform(sample_data)

        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["sepal_length_cm"]
        assert len(result) == len(sample_data)


class TestSpeciesEncoder:
    """Pruebas para SpeciesEncoder."""

    def test_init(self) -> None:
        """Prueba la inicialización del codificador."""
        encoder = SpeciesEncoder()
        assert "Iris-setosa" in encoder.species_mapping
        assert encoder.species_mapping["Iris-setosa"] == 0

    def test_fit(self, sample_labels: pd.Series) -> None:
        """Prueba el método fit."""
        encoder = SpeciesEncoder()
        result = encoder.fit(sample_labels)
        assert result is encoder  # Debe retornar self

    def test_transform(self, sample_labels: pd.Series) -> None:
        """Prueba el método transform."""
        encoder = SpeciesEncoder()
        encoder.fit(sample_labels)
        result = encoder.transform(sample_labels)

        assert result[0] == 0  # Iris-setosa
        assert result[1] == 0  # Iris-setosa
        assert result[2] == 1  # Iris-versicolor

    def test_inverse_transform(self) -> None:
        """Prueba inverse_transform."""
        encoder = SpeciesEncoder()
        encoded = [0, 1, 2]
        result = encoder.inverse_transform(encoded)

        assert result == ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]

    def test_round_trip(self, sample_labels: pd.Series) -> None:
        """Prueba que encode/decode sea idempotente."""
        encoder = SpeciesEncoder()
        encoder.fit(sample_labels)
        encoded = encoder.transform(sample_labels)
        decoded = encoder.inverse_transform(encoded)

        assert list(decoded) == list(sample_labels)

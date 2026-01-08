"""Pruebas unitarias para el cargador de datos."""

from pathlib import Path

import pandas as pd
import pytest

from iris_ml.utils.data_loader import load_iris_data, prepare_data


class TestLoadIrisData:
    """Pruebas para load_iris_data."""

    def test_load_default_path(self) -> None:
        """Prueba cargar datos con la ruta por defecto."""
        df = load_iris_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "species" in df.columns.str.lower().str.lower().values

    def test_load_custom_path(self) -> None:
        """Prueba cargar datos con una ruta personalizada."""
        data_path = Path(__file__).parent.parent.parent / "Iris.csv"
        df = load_iris_data(data_path)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_load_nonexistent_file(self) -> None:
        """Prueba que se lance error con archivo inexistente."""
        fake_path = Path("/fake/path/data.csv")
        with pytest.raises(FileNotFoundError):
            load_iris_data(fake_path)


class TestPrepareData:
    """Pruebas para prepare_data."""

    def test_prepare_data_returns_tuple(self) -> None:
        """Prueba que prepare_data retorna una tupla."""
        result = prepare_data(test_size=0.2, random_state=42)
        assert isinstance(result, tuple)
        assert len(result) == 4

    def test_prepare_data_shapes(self) -> None:
        """Prueba las dimensiones de los datos preparados."""
        X_train, X_test, y_train, y_test = prepare_data(test_size=0.2, random_state=42)

        assert isinstance(X_train, pd.DataFrame)
        assert isinstance(X_test, pd.DataFrame)
        assert isinstance(y_train, pd.Series)
        assert isinstance(y_test, pd.Series)

        assert len(X_train) == len(y_train)
        assert len(X_test) == len(y_test)

    def test_prepare_data_features(self) -> None:
        """Prueba que los datos tengan las características correctas."""
        X_train, _, _, _ = prepare_data(test_size=0.2, random_state=42)

        expected_features = [
            "sepal_length_cm",
            "sepal_width_cm",
            "petal_length_cm",
            "petal_width_cm",
        ]

        for feature in expected_features:
            assert feature in X_train.columns

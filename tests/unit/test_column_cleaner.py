"""Pruebas unitarias para el limpiador de columnas."""

import pandas as pd
import pytest

from iris_ml.utils.column_cleaner import clean_column_names, _to_snake_case


class TestToSnakeCase:
    """Pruebas para la función _to_snake_case."""

    def test_pascal_case(self) -> None:
        """Prueba conversión de PascalCase."""
        assert _to_snake_case("SepalLengthCm") == "sepal_length_cm"
        assert _to_snake_case("PetalWidth") == "petal_width"
        assert _to_snake_case("Id") == "id"

    def test_camel_case(self) -> None:
        """Prueba conversión de camelCase."""
        assert _to_snake_case("sepalLengthCm") == "sepal_length_cm"
        assert _to_snake_case("petalWidth") == "petal_width"

    def test_upper_case(self) -> None:
        """Prueba conversión de UPPER_CASE."""
        assert _to_snake_case("SEPAL_LENGTH") == "sepal_length"
        assert _to_snake_case("ID_NUMBER") == "id_number"

    def test_with_numbers(self) -> None:
        """Prueba manejo de números."""
        assert _to_snake_case("Width2") == "width_2"
        assert _to_snake_case("2Width") == "2_width"
        assert _to_snake_case("Test123Value") == "test_123_value"

    def test_already_snake_case(self) -> None:
        """Prueba que snake_case se mantiene."""
        assert _to_snake_case("sepal_length_cm") == "sepal_length_cm"
        assert _to_snake_case("petal_width") == "petal_width"

    def test_with_spaces(self) -> None:
        """Prueba manejo de espacios."""
        assert _to_snake_case("Sepal Length Cm") == "sepal_length_cm"
        assert _to_snake_case("  Petal Width  ") == "petal_width"

    def test_with_special_characters(self) -> None:
        """Prueba manejo de caracteres especiales."""
        assert _to_snake_case("Sepal-Length-Cm") == "sepal_length_cm"
        assert _to_snake_case("Petal@Width#2") == "petalwidth_2"

    def test_empty_string(self) -> None:
        """Prueba con string vacío."""
        assert _to_snake_case("") == ""

    def test_single_word(self) -> None:
        """Prueba con una sola palabra."""
        assert _to_snake_case("Species") == "species"
        assert _to_snake_case("ID") == "id"


class TestCleanColumnNames:
    """Pruebas para la función clean_column_names."""

    def test_pascal_case_columns(self) -> None:
        """Prueba con columnas en PascalCase."""
        df = pd.DataFrame(
            columns=["Id", "SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "Species"]
        )
        result = clean_column_names(df)

        expected = ["id", "sepal_length_cm", "sepal_width_cm", "petal_length_cm", "species"]
        assert list(result.columns) == expected

    def test_camel_case_columns(self) -> None:
        """Prueba con columnas en camelCase."""
        df = pd.DataFrame(columns=["id", "sepalLengthCm", "petalWidth"])
        result = clean_column_names(df)

        expected = ["id", "sepal_length_cm", "petal_width"]
        assert list(result.columns) == expected

    def test_with_numbers(self) -> None:
        """Prueba con columnas que tienen números."""
        df = pd.DataFrame(columns=["Width2", "Test123Value", "2Number"])
        result = clean_column_names(df)

        expected = ["width_2", "test_123_value", "2_number"]
        assert list(result.columns) == expected

    def test_already_snake_case(self) -> None:
        """Prueba que snake_case se mantiene."""
        df = pd.DataFrame(columns=["sepal_length_cm", "petal_width", "species"])
        result = clean_column_names(df)

        expected = ["sepal_length_cm", "petal_width", "species"]
        assert list(result.columns) == expected

    def test_with_spaces(self) -> None:
        """Prueba con columnas que tienen espacios."""
        df = pd.DataFrame(columns=["  Sepal Length  ", "Petal Width", "Species"])
        result = clean_column_names(df)

        expected = ["sepal_length", "petal_width", "species"]
        assert list(result.columns) == expected

    def test_preserves_data(self) -> None:
        """Prueba que los datos se preservan."""
        df = pd.DataFrame(
            {"SepalLengthCm": [5.1, 4.9], "PetalWidth": [0.2, 0.2]},
            columns=["SepalLengthCm", "PetalWidth"],
        )
        result = clean_column_names(df)

        assert list(result["sepal_length_cm"]) == [5.1, 4.9]
        assert list(result["petal_width"]) == [0.2, 0.2]

    def test_real_iris_columns(self) -> None:
        """Prueba con las columnas reales del dataset Iris."""
        df = pd.DataFrame(
            columns=[
                "Id",
                "SepalLengthCm",
                "SepalWidthCm",
                "PetalLengthCm",
                "PetalWidthCm",
                "Species",
            ]
        )
        result = clean_column_names(df)

        expected = [
            "id",
            "sepal_length_cm",
            "sepal_width_cm",
            "petal_length_cm",
            "petal_width_cm",
            "species",
        ]
        assert list(result.columns) == expected

"""Pruebas unitarias para el pipeline."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from iris_ml.models import IrisPipeline, create_pipeline


class TestIrisPipeline:
    """Pruebas para IrisPipeline."""

    def test_init(self) -> None:
        """Prueba la inicialización del pipeline."""
        pipeline = IrisPipeline(n_estimators=50, random_state=42)
        assert pipeline.pipeline is not None
        assert pipeline.species_encoder is not None

    def test_fit(self, sample_data: pd.DataFrame, sample_labels: pd.Series) -> None:
        """Prueba el entrenamiento del pipeline."""
        pipeline = IrisPipeline(n_estimators=10, random_state=42)
        result = pipeline.fit(sample_data, sample_labels)

        assert result is pipeline  # Debe retornar self

    def test_predict(
        self, trained_pipeline: IrisPipeline, sample_data: pd.DataFrame
    ) -> None:
        """Prueba las predicciones."""
        predictions = trained_pipeline.predict(sample_data)

        assert isinstance(predictions, list)
        assert len(predictions) == len(sample_data)
        assert all(isinstance(pred, str) for pred in predictions)
        assert all(
            pred in ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
            for pred in predictions
        )

    def test_predict_proba(
        self, trained_pipeline: IrisPipeline, sample_data: pd.DataFrame
    ) -> None:
        """Prueba las probabilidades de predicción."""
        probabilities = trained_pipeline.predict_proba(sample_data)

        assert isinstance(probabilities, pd.DataFrame)
        assert len(probabilities) == len(sample_data)
        assert all(
            col in probabilities.columns
            for col in ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
        )

    def test_score(
        self,
        trained_pipeline: IrisPipeline,
        sample_data: pd.DataFrame,
        sample_labels: pd.Series,
    ) -> None:
        """Prueba el cálculo de precisión."""
        score = trained_pipeline.score(sample_data, sample_labels)

        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_save_and_load(
        self, trained_pipeline: IrisPipeline, sample_data: pd.DataFrame
    ) -> None:
        """Prueba guardar y cargar el modelo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_model.pkl"
            trained_pipeline.save(filepath)

            assert filepath.exists()

            # Cargar modelo
            loaded_pipeline = IrisPipeline.load(filepath)

            # Verificar que las predicciones sean iguales
            original_preds = trained_pipeline.predict(sample_data)
            loaded_preds = loaded_pipeline.predict(sample_data)

            assert original_preds == loaded_preds


class TestCreatePipeline:
    """Pruebas para create_pipeline."""

    def test_create_pipeline_default(self) -> None:
        """Prueba crear pipeline con valores por defecto."""
        pipeline = create_pipeline()
        assert isinstance(pipeline, IrisPipeline)

    def test_create_pipeline_with_params(self) -> None:
        """Prueba crear pipeline con parámetros personalizados."""
        pipeline = create_pipeline(n_estimators=50, random_state=123)
        assert isinstance(pipeline, IrisPipeline)

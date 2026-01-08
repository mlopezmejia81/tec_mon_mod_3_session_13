"""Pruebas de integración para el pipeline de entrenamiento."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from iris_ml.models import IrisPipeline
from iris_ml.utils.data_loader import prepare_data


class TestTrainingPipeline:
    """Pruebas de integración para el pipeline completo de entrenamiento."""

    def test_end_to_end_training(self) -> None:
        """Prueba el flujo completo de entrenamiento."""
        # Preparar datos
        X_train, X_test, y_train, y_test = prepare_data(
            test_size=0.2, random_state=42
        )

        # Crear y entrenar pipeline
        pipeline = IrisPipeline(n_estimators=10, random_state=42)
        pipeline.fit(X_train, y_train)

        # Evaluar
        train_score = pipeline.score(X_train, y_train)
        test_score = pipeline.score(X_test, y_test)

        # Verificaciones
        assert train_score >= 0.0
        assert test_score >= 0.0
        assert train_score <= 1.0
        assert test_score <= 1.0

    def test_training_with_save_and_load(self) -> None:
        """Prueba entrenamiento con guardado y carga."""
        # Preparar datos
        X_train, X_test, y_train, y_test = prepare_data(
            test_size=0.2, random_state=42
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            # Entrenar y guardar
            pipeline = IrisPipeline(n_estimators=10, random_state=42)
            pipeline.fit(X_train, y_train)
            original_score = pipeline.score(X_test, y_test)

            model_path = Path(tmpdir) / "model.pkl"
            pipeline.save(model_path)

            # Cargar y verificar
            loaded_pipeline = IrisPipeline.load(model_path)
            loaded_score = loaded_pipeline.score(X_test, y_test)

            assert abs(original_score - loaded_score) < 0.01

    def test_pipeline_consistency(self) -> None:
        """Prueba la consistencia del pipeline entre entrenamientos."""
        X_train, X_test, y_train, y_test = prepare_data(
            test_size=0.2, random_state=42
        )

        # Entrenar dos veces con la misma semilla
        pipeline1 = IrisPipeline(n_estimators=10, random_state=42)
        pipeline1.fit(X_train, y_train)

        pipeline2 = IrisPipeline(n_estimators=10, random_state=42)
        pipeline2.fit(X_train, y_train)

        # Las predicciones deben ser idénticas
        pred1 = pipeline1.predict(X_test)
        pred2 = pipeline2.predict(X_test)

        assert pred1 == pred2

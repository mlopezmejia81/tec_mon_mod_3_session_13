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
        # pipeline.score() retorna la precisión (accuracy) que siempre está entre 0.0 y 1.0
        # Verificamos que los scores sean válidos y que el modelo tenga un rendimiento mínimo
        assert 0.0 <= train_score <= 1.0, "Train score debe estar entre 0.0 y 1.0"
        assert 0.0 <= test_score <= 1.0, "Test score debe estar entre 0.0 y 1.0"
        # Para el dataset de Iris, esperamos al menos 80% de precisión (es un dataset relativamente fácil)
        assert test_score >= 0.8, f"El modelo debería tener al menos 80% de precisión, obtuvo {test_score:.2%}"

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

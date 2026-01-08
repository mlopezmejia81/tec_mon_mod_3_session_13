"""Script para entrenar el modelo de Iris."""

import sys
from pathlib import Path

import pandas as pd

from iris_ml.config import settings
from iris_ml.config.settings import get_model_path
from iris_ml.models import create_pipeline
from iris_ml.utils.data_loader import prepare_data


def main() -> int:
    """Función principal para entrenar el modelo.

    Returns:
        Código de salida (0 para éxito, 1 para error).
    """
    try:
        print("Cargando datos...")
        X_train, X_test, y_train, y_test = prepare_data()

        print("Creando pipeline...")
        pipeline = create_pipeline(n_estimators=100, random_state=settings.random_state)

        print("Entrenando modelo...")
        pipeline.fit(X_train, y_train)

        print("Evaluando modelo...")
        train_score = pipeline.score(X_train, y_train)
        test_score = pipeline.score(X_test, y_test)

        print(f"Precisión en entrenamiento: {train_score:.4f}")
        print(f"Precisión en prueba: {test_score:.4f}")

        print("Guardando modelo...")
        pipeline.save()

        model_path = get_model_path()
        print(f"Modelo guardado en: {model_path}")

        return 0

    except Exception as e:
        print(f"Error durante el entrenamiento: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

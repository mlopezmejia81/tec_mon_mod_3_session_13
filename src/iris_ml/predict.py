"""Script para realizar predicciones con el modelo entrenado."""

import sys
from pathlib import Path

import pandas as pd

from iris_ml.config import settings
from iris_ml.models import IrisPipeline


def main() -> int:
    """Función principal para realizar predicciones.

    Returns:
        Código de salida (0 para éxito, 1 para error).
    """
    try:
        # Cargar modelo
        print("Cargando modelo...")
        pipeline = IrisPipeline.load()

        # Ejemplo de predicción
        sample_data = pd.DataFrame(
            {
                "sepal_length_cm": [5.1, 6.2, 7.3],
                "sepal_width_cm": [3.5, 2.8, 3.0],
                "petal_length_cm": [1.4, 4.5, 6.1],
                "petal_width_cm": [0.2, 1.5, 2.5],
            }
        )

        print("\nPredicciones:")
        predictions = pipeline.predict(sample_data)
        probabilities = pipeline.predict_proba(sample_data)

        for i, pred in enumerate(predictions):
            print(f"\nMuestra {i+1}:")
            print(f"  Predicción: {pred}")
            print(f"  Probabilidades:")
            # probabilities es un DataFrame, usar iloc para acceder a cada fila
            prob_row = probabilities.iloc[i]
            for species, prob_value in prob_row.items():
                print(f"    {species}: {prob_value:.4f}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Primero necesitas entrenar el modelo ejecutando: iris-train", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"Error durante la predicción: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

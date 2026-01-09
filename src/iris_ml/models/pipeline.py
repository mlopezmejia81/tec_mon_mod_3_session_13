"""Pipeline completo para el modelo de clasificación de Iris."""

import pickle
from pathlib import Path
from typing import Any, List, Optional

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from iris_ml.config import settings
from iris_ml.config.settings import get_model_path
from iris_ml.preprocessing import ColumnSelector, SpeciesEncoder


class IrisPipeline:
    """Pipeline completo para clasificación de Iris.

    Esta clase encapsula el pipeline completo de preprocesamiento
    y clasificación para el dataset de Iris.

    Attributes:
        pipeline: Pipeline de scikit-learn con preprocesamiento y modelo.
        species_encoder: Codificador de especies.
    """

    def __init__(self, n_estimators: Optional[int] = None, random_state: Optional[int] = None) -> None:
        """Inicializa el pipeline de Iris.

        Args:
            n_estimators: Número de árboles en el Random Forest.
                         Si es None, usa el valor de config.yml.
            random_state: Semilla para reproducibilidad.
                         Si es None, usa el valor de config.yml.
        """
        if n_estimators is None:
            # Intentar obtener de config.yml, si no existe usar default
            ml_config = getattr(settings, "ml", {})
            n_estimators = ml_config.get("n_estimators", 100) if isinstance(ml_config, dict) else 100
        if random_state is None:
            random_state = settings.random_state

        self.species_encoder: SpeciesEncoder = SpeciesEncoder()

        # Crear el pipeline
        self.pipeline: Pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=n_estimators,
                        random_state=random_state,
                        n_jobs=-1,
                    ),
                ),
            ]
        )

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "IrisPipeline":
        """Entrena el pipeline con los datos proporcionados.

        Args:
            X: DataFrame con características.
            y: Serie con etiquetas de especies.

        Returns:
            self: Instancia del pipeline entrenado.
        """
        # Codificar las especies
        y_encoded = self.species_encoder.transform(y)

        # Entrenar el pipeline
        self.pipeline.fit(X, y_encoded)

        return self

    def predict(self, X: pd.DataFrame) -> List[str]:
        """Realiza predicciones sobre nuevos datos.

        Args:
            X: DataFrame con características.

        Returns:
            Lista de nombres de especies predichas.
        """
        # Realizar predicción
        y_pred_encoded = self.pipeline.predict(X)

        # Decodificar las predicciones
        y_pred = self.species_encoder.inverse_transform(y_pred_encoded)

        return y_pred

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        """Obtiene probabilidades de predicción.

        Args:
            X: DataFrame con características.

        Returns:
            DataFrame con probabilidades para cada clase.
        """
        proba = self.pipeline.predict_proba(X)
        species_names = list(self.species_encoder.species_mapping.keys())

        return pd.DataFrame(proba, columns=species_names)

    def score(self, X: pd.DataFrame, y: pd.Series) -> float:
        """Calcula la precisión del modelo.

        Args:
            X: DataFrame con características.
            y: Serie con etiquetas reales.

        Returns:
            Precisión del modelo.
        """
        y_encoded = self.species_encoder.transform(y)
        return self.pipeline.score(X, y_encoded)

    def save(self, filepath: Optional[Path] = None) -> None:
        """Guarda el modelo entrenado en un archivo.

        Args:
            filepath: Ruta donde guardar el modelo.
        """
        if filepath is None:
            filepath = get_model_path()

        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "wb") as f:
            pickle.dump(
                {
                    "pipeline": self.pipeline,
                    "species_encoder": self.species_encoder,
                },
                f,
            )

    @classmethod
    def load(cls, filepath: Optional[Path] = None) -> "IrisPipeline":
        """Carga un modelo entrenado desde un archivo.

        Args:
            filepath: Ruta al archivo del modelo.

        Returns:
            Instancia del pipeline cargado.
        """
        if filepath is None:
            filepath = get_model_path()

        if not filepath.exists():
            raise FileNotFoundError(f"El archivo {filepath} no existe.")

        with open(filepath, "rb") as f:
            model_data = pickle.load(f)

        instance = cls()
        instance.pipeline = model_data["pipeline"]
        instance.species_encoder = model_data["species_encoder"]

        return instance


def create_pipeline(**kwargs: Any) -> IrisPipeline:
    """Crea una instancia del pipeline de Iris.

    Args:
        **kwargs: Argumentos adicionales para el pipeline.

    Returns:
        Instancia del pipeline de Iris.
    """
    return IrisPipeline(**kwargs)

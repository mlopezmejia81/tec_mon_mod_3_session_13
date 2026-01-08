"""Esquemas Pydantic para la API."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class IrisFeatures(BaseModel):
    """Esquema para las características de una flor de Iris.

    Attributes:
        sepal_length_cm: Longitud del sépalo en centímetros.
        sepal_width_cm: Ancho del sépalo en centímetros.
        petal_length_cm: Longitud del pétalo en centímetros.
        petal_width_cm: Ancho del pétalo en centímetros.
    """

    sepal_length_cm: float = Field(
        ..., ge=0.0, le=20.0, description="Longitud del sépalo en centímetros"
    )
    sepal_width_cm: float = Field(
        ..., ge=0.0, le=20.0, description="Ancho del sépalo en centímetros"
    )
    petal_length_cm: float = Field(
        ..., ge=0.0, le=20.0, description="Longitud del pétalo en centímetros"
    )
    petal_width_cm: float = Field(
        ..., ge=0.0, le=20.0, description="Ancho del pétalo en centímetros"
    )

    @field_validator("sepal_length_cm", "sepal_width_cm", "petal_length_cm", "petal_width_cm")
    @classmethod
    def validate_positive(cls, v: float) -> float:
        """Valida que los valores sean positivos.

        Args:
            v: Valor a validar.

        Returns:
            Valor validado.

        Raises:
            ValueError: Si el valor no es positivo.
        """
        if v < 0:
            raise ValueError("Los valores deben ser positivos")
        return v


class PredictionRequest(BaseModel):
    """Esquema para solicitud de predicción.

    Attributes:
        features: Características de la flor de Iris.
    """

    features: IrisFeatures


class ProbabilityPrediction(BaseModel):
    """Esquema para probabilidad de predicción.

    Attributes:
        species: Nombre de la especie.
        probability: Probabilidad de pertenencia a esta especie.
    """

    species: str
    probability: float


class PredictionResponse(BaseModel):
    """Esquema para respuesta de predicción.

    Attributes:
        predicted_species: Especie predicha.
        probabilities: Lista de probabilidades para cada especie.
    """

    predicted_species: Literal["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
    probabilities: list[ProbabilityPrediction]


class HealthResponse(BaseModel):
    """Esquema para respuesta de health check.

    Attributes:
        status: Estado del servicio.
        version: Versión de la aplicación.
    """

    status: str
    version: str

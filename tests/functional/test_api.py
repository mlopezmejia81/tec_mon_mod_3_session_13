"""Pruebas funcionales para la API."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from iris_ml.api.main import app
from iris_ml.models import IrisPipeline
from iris_ml.utils.data_loader import prepare_data


@pytest.fixture
def trained_model_for_api():
    """Fixture que entrena un modelo para pruebas de API."""
    X_train, _, y_train, _ = prepare_data(test_size=0.2, random_state=42)
    pipeline = IrisPipeline(n_estimators=10, random_state=42)
    pipeline.fit(X_train, y_train)

    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = Path(tmpdir) / "model.pkl"
        pipeline.save(model_path)
        yield model_path


@pytest.fixture
def client(trained_model_for_api, monkeypatch):
    """Fixture que crea un cliente de prueba para la API."""
    # Temporalmente modificar el path del modelo usando monkeypatch
    import iris_ml.api.main as api_main
    from iris_ml.models import IrisPipeline

    # Limpiar el modelo global
    api_main._model = None

    # Precargar el modelo directamente
    try:
        api_main._model = IrisPipeline.load(trained_model_for_api)
    except Exception:
        api_main._model = None

    # Crear cliente de prueba
    # Usar base_url explícito para evitar problemas de compatibilidad
    client = TestClient(app, base_url="http://testserver")

    yield client

    # Restaurar
    api_main._model = None


class TestAPIEndpoints:
    """Pruebas funcionales para los endpoints de la API."""

    def test_root_endpoint(self, client) -> None:
        """Prueba el endpoint raíz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_health_endpoint(self, client) -> None:
        """Prueba el endpoint de health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert "version" in data

    def test_predict_endpoint_single(self, client) -> None:
        """Prueba el endpoint de predicción individual."""
        request_data = {
            "features": {
                "sepal_length_cm": 5.1,
                "sepal_width_cm": 3.5,
                "petal_length_cm": 1.4,
                "petal_width_cm": 0.2,
            }
        }

        response = client.post("/predict", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert "predicted_species" in data
        assert data["predicted_species"] in [
            "Iris-setosa",
            "Iris-versicolor",
            "Iris-virginica",
        ]
        assert "probabilities" in data
        assert len(data["probabilities"]) == 3

    def test_predict_endpoint_batch(self, client) -> None:
        """Prueba el endpoint de predicción en lote."""
        request_data = [
            {
                "features": {
                    "sepal_length_cm": 5.1,
                    "sepal_width_cm": 3.5,
                    "petal_length_cm": 1.4,
                    "petal_width_cm": 0.2,
                }
            },
            {
                "features": {
                    "sepal_length_cm": 6.2,
                    "sepal_width_cm": 2.8,
                    "petal_length_cm": 4.5,
                    "petal_width_cm": 1.5,
                }
            },
        ]

        response = client.post("/predict/batch", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

        for prediction in data:
            assert "predicted_species" in prediction
            assert "probabilities" in prediction

    def test_predict_endpoint_validation_error(self, client) -> None:
        """Prueba validación de datos incorrectos."""
        request_data = {
            "features": {
                "sepal_length_cm": -5.0,  # Valor negativo (inválido)
                "sepal_width_cm": 3.5,
                "petal_length_cm": 1.4,
                "petal_width_cm": 0.2,
            }
        }

        response = client.post("/predict", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_predict_endpoint_missing_field(self, client) -> None:
        """Prueba con campo faltante."""
        request_data = {
            "features": {
                "sepal_length_cm": 5.1,
                "sepal_width_cm": 3.5,
                # Faltan petal_length_cm y petal_width_cm
            }
        }

        response = client.post("/predict", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_api_docs_endpoint(self, client) -> None:
        """Prueba que la documentación esté disponible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_api_redoc_endpoint(self, client) -> None:
        """Prueba que ReDoc esté disponible."""
        response = client.get("/redoc")
        assert response.status_code == 200

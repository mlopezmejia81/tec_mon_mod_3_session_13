"""API principal con FastAPI para clasificación de especies de Iris.

FLUJO Y FUNCIONAMIENTO:
=======================

1. CARGA DEL MODELO:
   - El modelo se carga automáticamente la primera vez que se hace una predicción
   - Se guarda en la variable global `_model` para reutilizarlo en siguientes peticiones
   - Si el modelo no existe, se retorna error HTTP 503

2. ENDPOINTS DISPONIBLES:
   - GET /: Endpoint raíz con información básica del servicio
   - GET /health: Verifica el estado del servicio y si el modelo está cargado
   - POST /predict: Realiza una predicción individual de especie de Iris

3. FLUJO DE PREDICCIÓN:
   a) Cliente envía request con características de la flor (sepal_length, sepal_width, petal_length, petal_width)
   b) El endpoint valida el request usando Pydantic schemas
   c) Se convierte el request a DataFrame de pandas
   d) Se llama a `model.predict()` para obtener la especie predicha
   e) Se llama a `model.predict_proba()` para obtener las probabilidades de cada especie
   f) Se formatea la respuesta con la especie predicha y las probabilidades
   g) Se retorna la respuesta al cliente

4. GESTIÓN DE ERRORES:
   - Si el modelo no está disponible: HTTP 503 (Service Unavailable)
   - Si hay error durante la predicción: HTTP 500 (Internal Server Error)
   - Validación automática de datos de entrada mediante Pydantic

5. CONFIGURACIÓN:
   - Host, puerto y reload se obtienen de config.yml (vía Dynaconf)
   - Si no están configurados, se usan valores por defecto

ARCHIVOS RELACIONADOS:
- iris_ml/models/pipeline.py: Clase IrisPipeline que contiene el modelo entrenado
- iris_ml/api/schemas.py: Esquemas Pydantic para request/response
- iris_ml/config/settings.py: Configuración del proyecto (host, port, etc.)
"""

from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException

from iris_ml import __version__
from iris_ml.api.schemas import HealthResponse, PredictionRequest, PredictionResponse
from iris_ml.config import settings
from iris_ml.models import IrisPipeline

# Variable global para el modelo (se carga la primera vez que se necesita)
_model: Optional[IrisPipeline] = None


def load_model() -> IrisPipeline:
    """Carga el modelo entrenado.
    
    El modelo se carga solo una vez gracias al guard `if _model is None`.
    En la primera llamada, se carga desde el archivo y se guarda en `_model`.
    En siguientes llamadas, se reutiliza el modelo ya cargado.

    Returns:
        Instancia del modelo cargado.

    Raises:
        FileNotFoundError: Si el modelo no existe.
    """
    global _model
    if _model is None:
        _model = IrisPipeline.load()
    return _model


# Inicializar FastAPI
app = FastAPI(
    title="Iris ML Classification API",
    description="API REST para clasificación de especies de Iris usando Machine Learning",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/", response_model=HealthResponse, tags=["Health"])
async def root() -> HealthResponse:
    """Endpoint raíz con información del servicio.

    Returns:
        Información del estado del servicio.
    """
    return HealthResponse(status="healthy", version=__version__)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Endpoint de health check.

    Returns:
        Estado del servicio.
    """
    model_loaded = _model is not None
    status = "healthy" if model_loaded else "degraded"
    return HealthResponse(status=status, version=__version__)


@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict(request: PredictionRequest) -> PredictionResponse:
    """Realiza una predicción de especie de Iris.

    Args:
        request: Solicitud con características de la flor.

    Returns:
        Predicción con probabilidades.

    Raises:
        HTTPException: Si el modelo no está disponible o hay un error.
    """
    try:
        model = load_model()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    try:
        # Convertir a DataFrame
        features_dict = request.features.model_dump()
        df = pd.DataFrame([features_dict])

        # Realizar predicción
        prediction = model.predict(df)[0]
        probabilities_df = model.predict_proba(df)

        # Formatear respuesta
        probabilities_list = [
            {"species": species, "probability": float(prob)}
            for species, prob in probabilities_df.iloc[0].items()
        ]

        return PredictionResponse(
            predicted_species=prediction,  # type: ignore
            probabilities=probabilities_list,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {str(e)}")


def run_server(host: Optional[str] = None, port: Optional[int] = None, reload: Optional[bool] = None) -> None:
    """Ejecuta el servidor de desarrollo.

    Args:
        host: Host donde escuchar. Si es None, usa config.yml.
        port: Puerto donde escuchar. Si es None, usa config.yml.
        reload: Si se debe recargar automáticamente. Si es None, usa config.yml.
    """
    import uvicorn

    # Obtener configuración del API desde config.yml
    api_config = getattr(settings, "api", {})
    if not isinstance(api_config, dict):
        api_config = {}

    if host is None:
        host = api_config.get("host", "0.0.0.0")
    if port is None:
        port = api_config.get("port", 8000)
    if reload is None:
        reload = api_config.get("reload", settings.debug)

    log_level = api_config.get("log_level", "info")

    uvicorn.run(
        "iris_ml.api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
    )


if __name__ == "__main__":
    run_server()

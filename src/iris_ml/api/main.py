"""API principal con FastAPI."""

import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from iris_ml import __version__
from iris_ml.api.schemas import HealthResponse, PredictionRequest, PredictionResponse
from iris_ml.config import settings
from iris_ml.models import IrisPipeline

# Variable global para el modelo
_model: Optional[IrisPipeline] = None


def load_model() -> IrisPipeline:
    """Carga el modelo entrenado.

    Returns:
        Instancia del modelo cargado.

    Raises:
        FileNotFoundError: Si el modelo no existe.
    """
    global _model
    if _model is None:
        try:
            _model = IrisPipeline.load()
        except FileNotFoundError:
            raise FileNotFoundError(
                "El modelo no está disponible. Por favor, entrena el modelo primero."
            )
    return _model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación.

    Args:
        app: Instancia de FastAPI.

    Yields:
        None
    """
    # Startup: Cargar modelo al iniciar
    try:
        load_model()
        print("Modelo cargado exitosamente")
    except FileNotFoundError as e:
        print(f"Advertencia: {e}", file=sys.stderr)
        print(
            "La API funcionará, pero las predicciones fallarán hasta que el modelo sea entrenado",
            file=sys.stderr,
        )

    yield

    # Shutdown: Limpiar recursos si es necesario
    global _model
    _model = None


# Inicializar FastAPI con lifespan
app = FastAPI(
    title="Iris ML Classification API",
    description="API REST para clasificación de especies de Iris usando Machine Learning",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.post("/predict/batch", tags=["Predictions"])
async def predict_batch(requests: List[PredictionRequest]) -> List[PredictionResponse]:
    """Realiza predicciones en lote.

    Args:
        requests: Lista de solicitudes con características.

    Returns:
        Lista de predicciones con probabilidades.

    Raises:
        HTTPException: Si el modelo no está disponible o hay un error.
    """
    try:
        model = load_model()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    try:
        # Convertir a DataFrame
        features_list = [req.features.model_dump() for req in requests]
        df = pd.DataFrame(features_list)

        # Realizar predicciones
        predictions = model.predict(df)
        probabilities_df = model.predict_proba(df)

        # Formatear respuestas
        responses = []
        for i, prediction in enumerate(predictions):
            probabilities_list = [
                {"species": species, "probability": float(prob)}
                for species, prob in probabilities_df.iloc[i].items()
            ]
            responses.append(
                PredictionResponse(
                    predicted_species=prediction,  # type: ignore
                    probabilities=probabilities_list,
                )
            )

        return responses

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

# Guía de Desarrollo

## Estructura del Proyecto

El proyecto sigue una estructura modular clara:

```
src/iris_ml/
├── api/              # API REST con FastAPI
├── config/           # Configuración con Dynaconf
├── models/           # Modelos de ML y pipelines
├── preprocessing/    # Transformers personalizados
└── utils/            # Utilidades y helpers
```

## Patrones de Diseño Implementados

### 1. Pipeline Pattern

Usamos el patrón Pipeline de scikit-learn para encadenar transformaciones:

```python
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier())
])
```

### 2. Transformer Pattern

Transformers personalizados heredan de `BaseEstimator` y `TransformerMixin`:

```python
class CustomTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Transformación
        return X_transformed
```

### 3. Factory Pattern

Función factory para crear pipelines:

```python
def create_pipeline(**kwargs):
    return IrisPipeline(**kwargs)
```

### 4. Repository Pattern

Separación entre carga de datos y lógica de negocio en `utils/data_loader.py`.

## Convenciones de Código

### Type Hints

Siempre usar type hints:

```python
def example(x: int, y: str) -> bool:
    return True
```

### Docstrings

Siempre usar estilo Google:

```python
def example(x: int, y: str) -> bool:
    """Descripción breve.
    
    Args:
        x: Descripción de x.
        y: Descripción de y.
    
    Returns:
        Descripción del retorno.
    """
    return True
```

### Naming Conventions

- Clases: `PascalCase`
- Funciones/variables: `snake_case`
- Constantes: `UPPER_SNAKE_CASE`
- Privados: `_leading_underscore`

## Configuración

### Dynaconf

La configuración se maneja con Dynaconf:

```python
from iris_ml.config import settings

# Acceder a valores
debug = settings.debug
log_level = settings.log_level
```

### Entornos

- `development`: Desarrollo local
- `testing`: Pruebas automatizadas
- `production`: Producción

Cambiar entorno:
```bash
export DYNACONF_ENV=production
```

## Testing

### Estructura de Pruebas

- `tests/unit/`: Pruebas unitarias de componentes individuales
- `tests/integration/`: Pruebas de integración entre componentes
- `tests/functional/`: Pruebas funcionales end-to-end

### Fixtures

Usar fixtures compartidas en `conftest.py`:

```python
@pytest.fixture
def sample_data():
    return pd.DataFrame(...)
```

### Coverage

Mantener cobertura > 80%:

```bash
poetry run pytest --cov=src/iris_ml --cov-report=html
```

## CI/CD

GitHub Actions ejecuta:

1. **Linting**: pycodestyle, pydocstyle, black, mypy
2. **Testing**: pytest con múltiples versiones de Python
3. **Build**: Construcción del paquete

## Debugging

### Logging

Usar el nivel de log configurado:

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Mensaje de debug")
logger.info("Mensaje informativo")
logger.warning("Advertencia")
logger.error("Error")
```

### Debug Mode

Activar modo debug en configuración:

```toml
[development]
debug = true
log_level = "DEBUG"
```

## Dependencias

### Gestión con Poetry

Agregar dependencia:
```bash
poetry add nombre-paquete
```

Agregar dependencia de desarrollo:
```bash
poetry add --group dev nombre-paquete
```

Actualizar dependencias:
```bash
poetry update
```

## Comandos Útiles

Ver `Makefile` para comandos comunes:

```bash
make install      # Instalar dependencias
make test         # Ejecutar pruebas
make lint         # Ejecutar linters
make format       # Formatear código
make train        # Entrenar modelo
make api          # Iniciar API
```

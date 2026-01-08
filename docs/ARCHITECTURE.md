# Arquitectura del Proyecto

## Visión General

Este proyecto implementa un pipeline completo de Machine Learning para clasificación de especies de Iris, siguiendo las mejores prácticas de desarrollo en Python.

## Componentes Principales

### 1. Preprocesamiento (`preprocessing/`)

Implementa transformers personalizados usando `BaseEstimator` y `TransformerMixin` de scikit-learn:

- **ColumnSelector**: Selecciona columnas específicas del DataFrame
- **SpeciesEncoder**: Codifica/decodifica nombres de especies a valores numéricos

Estos transformers se integran perfectamente con los pipelines de scikit-learn.

### 2. Modelos (`models/`)

- **IrisPipeline**: Clase principal que encapsula el pipeline completo
  - Preprocesamiento (StandardScaler)
  - Clasificador (RandomForestClassifier)
  - Métodos para entrenar, predecir, guardar y cargar

### 3. Configuración (`config/`)

Usa Dynaconf para gestión de configuración:
- Configuración por entornos (development, testing, production)
- Variables de entorno
- Archivo `settings.toml`

### 4. API REST (`api/`)

FastAPI con:
- Endpoints REST
- Validación con Pydantic
- Documentación automática (Swagger/ReDoc)
- Esquemas de request/response

### 5. Utilidades (`utils/`)

Funciones auxiliares para:
- Cargar datos
- Preparar datasets para entrenamiento

## Flujo de Datos

```
Iris.csv
  ↓
DataLoader (carga y preparación)
  ↓
Pipeline (preprocesamiento + modelo)
  ↓
Modelo entrenado
  ↓
API REST (predicciones)
```

## Diseño Orientado a Objetos

### Principios aplicados:

1. **Encapsulación**: Cada clase tiene responsabilidades claras
2. **Abstracción**: Interfaces claras (fit, transform, predict)
3. **Herencia**: Uso de clases base de scikit-learn
4. **Polimorfismo**: Transformers intercambiables

### Jerarquía de clases:

```
BaseEstimator (scikit-learn)
  └── ColumnSelector
  └── SpeciesEncoder

BaseEstimator + TransformerMixin
  └── ColumnSelector
  └── SpeciesEncoder

IrisPipeline
  ├── Pipeline (scikit-learn)
  └── SpeciesEncoder
```

## Buenas Prácticas Implementadas

1. **Type Hints**: Anotaciones de tipo en todas las funciones
2. **Docstrings**: Documentación completa estilo Google
3. **PEP 8**: Formato de código estándar
4. **Testing**: Cobertura completa con pytest
5. **CI/CD**: Automatización con GitHub Actions
6. **Gestión de dependencias**: Poetry con pyproject.toml (PEP 621)
7. **Configuración**: Dynaconf para diferentes entornos

## Patrones de Diseño

1. **Pipeline Pattern**: Pipeline de scikit-learn para preprocesamiento y modelado
2. **Factory Pattern**: `create_pipeline()` para crear instancias
3. **Repository Pattern**: Separación de datos y lógica
4. **Dependency Injection**: Configuración inyectada vía Dynaconf

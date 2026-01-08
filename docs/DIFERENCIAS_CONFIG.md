# Diferencias entre .env, config.yml, Dynaconf y Pydantic

## Resumen Rápido

| Característica | `.env` | `config.yml` | `Dynaconf` | `Pydantic` |
|---------------|--------|--------------|------------|------------|
| **Propósito** | Variables de entorno y secretos | Configuración estructurada | **Orquestador de configuración** | Validación de datos |
| **Formato** | Texto plano (KEY=VALUE) | YAML estructurado | **Biblioteca Python** | Clases Python |
| **Validación** | No | No | No | Sí (tipos, rangos, etc.) |
| **Secrets** | ✅ Ideal | ❌ No seguro | ✅ Lee de .env | ✅ Puede usar |
| **Estructura** | Plana | Anidada | **Unifica múltiples fuentes** | Orientada a objetos |
| **Uso Principal** | Credenciales, API keys | Configuración por entornos | **Gestiona configuración** | Validación de requests/responses |
| **Rol** | Archivo de datos | Archivo de datos | **Herramienta/Librería** | Herramienta/Librería |

## 🔑 Concepto Clave: Dynaconf es el ORQUESTADOR

**Dynaconf NO es un archivo, es una BIBLIOTECA que lee y unifica configuración desde múltiples fuentes:**

- ✅ Lee de `.env`
- ✅ Lee de `config.yml`
- ✅ Lee de `settings.toml`
- ✅ Lee de variables de entorno del sistema
- ✅ Unifica todo en un solo objeto `settings`

## 1. `.env` - Variables de Entorno

### ¿Qué es?
Archivo de texto plano con variables de entorno en formato `KEY=VALUE`.

### Características:
- ✅ **Simple**: Formato plano, fácil de leer
- ✅ **Secrets**: Ideal para credenciales y secretos
- ✅ **Portable**: Fácil de copiar entre entornos
- ❌ **Sin validación**: No valida tipos ni formatos
- ❌ **Sin estructura**: Solo pares clave-valor

### Ejemplo:
```bash
# .env
ENV_FOR_DYNACONF=development
SECRET_KEY=mi-clave-secreta-123
API_KEY=abc123xyz
DEBUG=true
DB_PASSWORD=super-secret-password
```

### Cuándo usar:
- ✅ Credenciales y secretos (API keys, passwords)
- ✅ Variables que cambian entre entornos
- ✅ Valores que NO deben versionarse en Git
- ✅ Configuración simple (strings, números, booleanos)

### Uso en código:
```python
from iris_ml.config import settings

# Dynaconf lee automáticamente desde .env
secret_key = settings.secret_key
api_key = settings.api_key
debug = settings.debug
```

---

## 2. `config.yml` - Configuración Estructurada

### ¿Qué es?
Archivo YAML con configuración estructurada y organizada por entornos.

### Características:
- ✅ **Estructurado**: Permite anidación y organización
- ✅ **Entornos**: Diferentes configuraciones por entorno
- ✅ **Versionable**: Puede estar en Git (sin secretos)
- ✅ **Legible**: Formato YAML fácil de leer
- ❌ **Sin validación**: No valida tipos automáticamente
- ❌ **No para secretos**: No debe contener credenciales

### Ejemplo:
```yaml
development:
  debug: true
  log_level: "DEBUG"
  data_path: "Iris.csv"
  ml:
    n_estimators: 50
    max_depth: null
  api:
    host: "0.0.0.0"
    port: 8000
    reload: true

production:
  debug: false
  log_level: "WARNING"
  ml:
    n_estimators: 200
  api:
    port: 8000
    reload: false
    workers: 4
```

### Cuándo usar:
- ✅ Configuración estructurada (objetos anidados)
- ✅ Valores que cambian por entorno
- ✅ Configuración no sensible (puertos, rutas, parámetros)
- ✅ Valores que SÍ pueden versionarse en Git

### Uso en código:
```python
from iris_ml.config import settings

# Acceder a valores anidados
n_estimators = settings.ml.n_estimators
api_port = settings.api.port
api_host = settings.api.host
```

---

## 3. Pydantic - Validación de Datos

### ¿Qué es?
Biblioteca de Python para validación de datos usando clases y type hints.

### Características:
- ✅ **Validación fuerte**: Tipos, rangos, formatos
- ✅ **Type safety**: Type hints integrados
- ✅ **Documentación**: Auto-genera documentación
- ✅ **Serialización**: Convierte a/desde JSON, dict
- ✅ **IDE support**: Autocompletado y type checking
- ❌ **Más complejo**: Requiere definir clases
- ❌ **No para configuración**: Principalmente para datos de entrada/salida

### Ejemplo:
```python
from pydantic import BaseModel, Field, field_validator

class IrisFeatures(BaseModel):
    sepal_length_cm: float = Field(ge=0.0, le=20.0)
    sepal_width_cm: float = Field(ge=0.0, le=20.0)
    petal_length_cm: float = Field(ge=0.0, le=20.0)
    petal_width_cm: float = Field(ge=0.0, le=20.0)
    
    @field_validator('sepal_length_cm')
    @classmethod
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError("Debe ser positivo")
        return v
```

### Cuándo usar:
- ✅ Validación de datos de entrada (API requests)
- ✅ Validación de datos de salida (API responses)
- ✅ Type safety en funciones
- ✅ Documentación automática (FastAPI)
- ❌ NO para configuración de aplicación

### Uso en código:
```python
# En FastAPI - Validación automática
@app.post("/predict")
async def predict(request: IrisFeatures):
    # Pydantic valida automáticamente
    # Si los datos son inválidos, retorna error 422
    return {"prediction": "Iris-setosa"}
```

---

## Comparación Práctica

### Escenario 1: Credenciales de API

**❌ NO usar config.yml:**
```yaml
# config.yml - MAL
api:
  key: "secret-key-123"  # ❌ No versionar secretos
```

**✅ SÍ usar .env:**
```bash
# .env - BIEN
API_KEY=secret-key-123  # ✅ No se versiona
```

**Uso:**
```python
from iris_ml.config import settings
api_key = settings.api_key  # Lee de .env
```

---

### Escenario 2: Configuración del Modelo ML

**❌ NO usar .env:**
```bash
# .env - MAL
ML_N_ESTIMATORS=100
ML_MAX_DEPTH=null
ML_MIN_SAMPLES_SPLIT=2
# ❌ Muy verboso para estructuras complejas
```

**✅ SÍ usar config.yml:**
```yaml
# config.yml - BIEN
ml:
  n_estimators: 100
  max_depth: null
  min_samples_split: 2
# ✅ Estructurado y legible
```

**Uso:**
```python
from iris_ml.config import settings
n_estimators = settings.ml.n_estimators
```

---

### Escenario 3: Validación de Request de API

**❌ NO usar .env o config.yml:**
```python
# ❌ No valida tipos ni rangos
data = request.json()
sepal_length = data["sepal_length_cm"]  # ¿Es float? ¿Está en rango?
```

**✅ SÍ usar Pydantic:**
```python
# ✅ Valida automáticamente
class IrisFeatures(BaseModel):
    sepal_length_cm: float = Field(ge=0.0, le=20.0)

@app.post("/predict")
async def predict(features: IrisFeatures):
    # Si sepal_length_cm < 0 o > 20, retorna error 422
    return {"prediction": "Iris-setosa"}
```

---

## Flujo Completo en el Proyecto

### 1. Configuración de la Aplicación

```python
# .env - Secretos
SECRET_KEY=mi-clave
API_KEY=abc123

# config.yml - Configuración estructurada
development:
  api:
    port: 8000
  ml:
    n_estimators: 50

# Código
from iris_ml.config import settings
secret = settings.secret_key  # De .env
port = settings.api.port      # De config.yml
```

### 2. Validación de Datos de Entrada

```python
# Pydantic - Validación
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    features: IrisFeatures

# FastAPI valida automáticamente
@app.post("/predict")
async def predict(request: PredictionRequest):
    # request ya está validado por Pydantic
    return {"prediction": "Iris-setosa"}
```

---

## Tabla de Decisión

| Necesitas... | Usa... | Ejemplo |
|--------------|--------|---------|
| Guardar una API key | `.env` | `API_KEY=abc123` |
| Configuración por entorno | `config.yml` | `development: { api: { port: 8000 } }` |
| Validar datos de entrada | `Pydantic` | `class Request(BaseModel): ...` |
| Secretos y passwords | `.env` | `DB_PASSWORD=secret` |
| Estructura anidada | `config.yml` | `ml: { n_estimators: 100 }` |
| Validar tipos y rangos | `Pydantic` | `Field(ge=0.0, le=20.0)` |
| Valores simples | `.env` | `DEBUG=true` |
| Documentación automática | `Pydantic` | FastAPI docs |

---

## 4. Dynaconf - Orquestador de Configuración

### ¿Qué es?
**Dynaconf es una BIBLIOTECA de Python** que lee y unifica configuración desde múltiples fuentes.

### Características:
- ✅ **Unificador**: Lee de .env, config.yml, settings.toml, variables de entorno
- ✅ **Prioridad**: Define orden de lectura (variables > .env > config.yml)
- ✅ **Entornos**: Cambia entre development, testing, production
- ✅ **Un solo punto de acceso**: Todo a través de `settings`
- ❌ **No valida**: No valida tipos ni formatos (eso es Pydantic)
- ❌ **No es un archivo**: Es código Python

### Ejemplo de Implementación:
```python
# src/iris_ml/config/settings.py
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["config.yml", "settings.toml"],  # Lee estos archivos
    load_dotenv=True,                                 # Lee .env
    dotenv_path=".env",                              # Ruta al .env
    environments=True,                                # Habilitar entornos
    default_env="development",                      # Entorno por defecto
    env_switcher="ENV_FOR_DYNACONF",               # Variable para cambiar entorno
)
```

### Cuándo usar:
- ✅ Necesitas leer configuración desde múltiples fuentes
- ✅ Quieres un solo punto de acceso (`settings`)
- ✅ Necesitas cambiar entre entornos fácilmente
- ✅ Quieres prioridad clara entre fuentes

### Uso en código:
```python
from iris_ml.config import settings

# Dynaconf unifica todo:
secret_key = settings.secret_key      # De .env
n_estimators = settings.ml.n_estimators  # De config.yml
debug = settings.debug                # De config.yml o .env (mayor prioridad)
```

---

## Comparación: Dynaconf vs Otros

### Dynaconf vs .env

| Aspecto | `.env` | `Dynaconf` |
|---------|--------|------------|
| **Tipo** | Archivo | Biblioteca |
| **Función** | Almacena datos | Lee y unifica datos |
| **Uso** | Escribir variables | Leer configuración |

**Relación**: Dynaconf **lee** de `.env`

### Dynaconf vs config.yml

| Aspecto | `config.yml` | `Dynaconf` |
|---------|--------------|------------|
| **Tipo** | Archivo | Biblioteca |
| **Función** | Almacena configuración | Lee y unifica configuración |
| **Uso** | Escribir YAML | Leer YAML |

**Relación**: Dynaconf **lee** de `config.yml`

### Dynaconf vs Pydantic

| Aspecto | `Dynaconf` | `Pydantic` |
|---------|------------|------------|
| **Propósito** | Gestionar configuración | Validar datos |
| **Cuándo** | Al inicio de la app | En requests/responses |
| **Validación** | No valida | Sí valida |
| **Uso** | `settings.debug` | `IrisFeatures(...)` |

**Relación**: Son **complementarios**, no competidores

---

## Flujo Completo en el Proyecto

```
┌─────────────┐
│   .env      │  ──┐
│ (secretos)  │    │
└─────────────┘    │
                   │
┌─────────────┐    │    ┌──────────────┐
│ config.yml  │  ──┼───▶│  Dynaconf    │
│ (config)    │    │    │  (settings)  │
└─────────────┘    │    └──────────────┘
                   │           │
┌─────────────┐    │           │
│settings.toml│  ──┘           │
│ (backup)    │                │
└─────────────┘                │
                                ▼
                        ┌──────────────┐
                        │   Código      │
                        │ settings.debug│
                        │ settings.ml...│
                        └──────────────┘
                                │
                                ▼
                        ┌──────────────┐
                        │   FastAPI    │
                        │  + Pydantic  │
                        │ (validación) │
                        └──────────────┘
```

### Paso a Paso:

1. **Dynaconf lee** de `.env`, `config.yml`, `settings.toml`
2. **Dynaconf unifica** todo en el objeto `settings`
3. **Tu código accede** a `settings.debug`, `settings.ml.n_estimators`
4. **Pydantic valida** los datos de entrada de la API (separado)

---

## Ejemplo Práctico Completo

### 1. Archivos de Configuración

```bash
# .env
SECRET_KEY=mi-clave-secreta
API_KEY=abc123
ENV_FOR_DYNACONF=development
```

```yaml
# config.yml
development:
  debug: true
  ml:
    n_estimators: 50
  api:
    port: 8000
```

### 2. Dynaconf Unifica Todo

```python
# src/iris_ml/config/settings.py
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["config.yml"],
    load_dotenv=True,
    dotenv_path=".env",
)
```

### 3. Uso en el Código

```python
from iris_ml.config import settings

# Dynaconf ya unificó todo:
secret = settings.secret_key        # De .env
debug = settings.debug              # De config.yml (development)
n_estimators = settings.ml.n_estimators  # De config.yml
api_port = settings.api.port       # De config.yml
```

### 4. Pydantic Valida Requests (Separado)

```python
from pydantic import BaseModel

class IrisFeatures(BaseModel):
    sepal_length_cm: float = Field(ge=0.0, le=20.0)

@app.post("/predict")
async def predict(features: IrisFeatures):  # Pydantic valida aquí
    # Usar configuración de Dynaconf
    n_estimators = settings.ml.n_estimators
    return {"prediction": "Iris-setosa"}
```

---

## Resumen

1. **`.env`**: Archivo con secretos → **Dynaconf lo lee**
2. **`config.yml`**: Archivo con configuración → **Dynaconf lo lee**
3. **`Dynaconf`**: Biblioteca que **unifica** .env y config.yml → **Proporciona `settings`**
4. **`Pydantic`**: Biblioteca que **valida** datos de API → **Separado de configuración**

**En este proyecto:**
- `.env` → Secretos (SECRET_KEY, API_KEY) → **Leído por Dynaconf**
- `config.yml` → Configuración (ml.n_estimators, api.port) → **Leído por Dynaconf**
- `Dynaconf` → **Unifica todo en `settings`** → **Usado en el código**
- `Pydantic` → Validación de requests de API (IrisFeatures) → **Separado**

### Analogía Simple:

- **`.env` y `config.yml`** = Los ingredientes (datos)
- **`Dynaconf`** = El cocinero (lee y combina ingredientes)
- **`settings`** = El plato final (resultado unificado)
- **`Pydantic`** = El crítico gastronómico (valida la calidad, pero es otro proceso)

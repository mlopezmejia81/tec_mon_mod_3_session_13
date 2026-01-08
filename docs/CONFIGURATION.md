# Guía de Configuración

Este proyecto usa Dynaconf para gestionar la configuración desde múltiples fuentes.

## Archivos de Configuración

### 1. `.env` - Variables de Entorno y Credenciales

**Ubicación**: Raíz del proyecto  
**Propósito**: Variables sensibles y secretos que NO deben versionarse

#### Crear el archivo:

```bash
# Copiar el archivo de ejemplo
cp env.example .env

# Editar con tus valores
nano .env
```

#### Variables importantes:

```bash
# Entorno de ejecución
ENV_FOR_DYNACONF=development  # development, testing, production

# Configuración de la aplicación
SECRET_KEY=your-secret-key-change-in-production
DEBUG=true

# Credenciales de API (si aplica)
API_KEY=your-api-key-here
API_SECRET=your-api-secret-here

# Configuración de base de datos (si aplica)
DATABASE_URL=sqlite:///./iris_ml.db
DB_PASSWORD=your-database-password

# Configuración del modelo
RANDOM_STATE=42
TEST_SIZE=0.2
```

**⚠️ IMPORTANTE**: El archivo `.env` está en `.gitignore` y NO debe subirse a Git.

### 2. `config.yml` - Configuración General

**Ubicación**: Raíz del proyecto  
**Propósito**: Configuración estructurada por entornos

#### Estructura:

```yaml
default: &default
  # Configuración común a todos los entornos
  debug: false
  log_level: "INFO"
  data_path: "Iris.csv"
  model_path: "models/iris_model.pkl"
  
  # Configuración del modelo ML
  ml:
    n_estimators: 100
    max_depth: null
  
  # Configuración de la API
  api:
    host: "0.0.0.0"
    port: 8000
    reload: false

development: &development
  <<: *default  # Hereda configuración de default
  debug: true
  log_level: "DEBUG"
  api:
    <<: *default
    reload: true  # Auto-reload en desarrollo

production: &production
  <<: *default
  debug: false
  log_level: "WARNING"
  api:
    <<: *default
    workers: 4  # Múltiples workers en producción
```

#### Entornos disponibles:

- **development**: Desarrollo local
- **testing**: Pruebas automatizadas
- **production**: Producción

### 3. `settings.toml` - Configuración Alternativa (Opcional)

**Ubicación**: Raíz del proyecto  
**Propósito**: Mantiene compatibilidad, configuración alternativa en TOML

Este archivo se lee como respaldo si `config.yml` no existe o no tiene ciertos valores.

## Prioridad de Configuración

Dynaconf lee la configuración en este orden (mayor a menor prioridad):

1. **Variables de entorno del sistema** (`export VARIABLE=value`)
2. **Archivo `.env`** (variables locales)
3. **`config.yml`** (configuración por entorno)
4. **`settings.toml`** (configuración alternativa)

### Ejemplo:

Si tienes:

```bash
# .env
DEBUG=true
API_PORT=8080
```

```yaml
# config.yml
development:
  api:
    port: 8000
```

El resultado será:
- `DEBUG=true` (de .env, tiene mayor prioridad)
- `api.port=8080` (de .env, tiene mayor prioridad sobre config.yml)

## Uso en el Código

### Acceder a la configuración:

```python
from iris_ml.config import settings

# Configuración básica
debug = settings.debug
log_level = settings.log_level
data_path = settings.data_path

# Configuración anidada (desde config.yml)
n_estimators = settings.ml.n_estimators
api_host = settings.api.host
api_port = settings.api.port

# Variables de entorno (desde .env)
secret_key = settings.secret_key
api_key = settings.api_key

# Con valores por defecto
max_depth = getattr(settings.ml, "max_depth", None)
```

### Funciones auxiliares:

```python
from iris_ml.config.settings import get_data_path, get_model_path, get_config

# Obtener rutas absolutas
data_path = get_data_path()  # Path object
model_path = get_model_path()  # Path object

# Obtener toda la configuración como dict
config = get_config()
```

## Cambiar Entorno

### Método 1: Variable en `.env`

```bash
# .env
ENV_FOR_DYNACONF=production
```

### Método 2: Variable de entorno del sistema

```bash
export ENV_FOR_DYNACONF=production
poetry run iris-api
```

### Método 3: Temporal (solo para un comando)

```bash
ENV_FOR_DYNACONF=testing poetry run pytest
```

## Ejemplos Prácticos

### Desarrollo Local

```bash
# .env
ENV_FOR_DYNACONF=development
DEBUG=true
SECRET_KEY=dev-secret-key
```

```yaml
# config.yml
development:
  api:
    reload: true  # Auto-reload activado
  ml:
    n_estimators: 50  # Menos árboles para desarrollo rápido
```

### Producción

```bash
# .env
ENV_FOR_DYNACONF=production
DEBUG=false
SECRET_KEY=production-secret-key-from-secrets-manager
API_KEY=production-api-key
```

```yaml
# config.yml
production:
  api:
    reload: false
    workers: 4  # Múltiples workers
  ml:
    n_estimators: 200  # Más árboles para mejor precisión
```

### Testing

```bash
# .env
ENV_FOR_DYNACONF=testing
DEBUG=true
```

```yaml
# config.yml
testing:
  test_size: 0.3
  ml:
    n_estimators: 10  # Muy pocos árboles para tests rápidos
```

## Buenas Prácticas

1. **Nunca versionar `.env`**: Ya está en `.gitignore`
2. **Versionar `env.example`**: Template con valores de ejemplo
3. **Versionar `config.yml`**: Configuración no sensible
4. **Usar `.env` para secretos**: Claves, passwords, tokens
5. **Usar `config.yml` para configuración**: Rutas, puertos, parámetros del modelo
6. **Documentar variables**: Comentar variables nuevas en `env.example`

## Solución de Problemas

### La configuración no se lee

1. Verifica que `.env` existe y tiene `ENV_FOR_DYNACONF`
2. Verifica que `config.yml` tiene la estructura correcta
3. Revisa el orden de prioridad de configuración

### El entorno no cambia

1. Verifica `ENV_FOR_DYNACONF` en `.env`
2. Asegúrate de reiniciar la aplicación después de cambiar `.env`
3. Verifica que el entorno existe en `config.yml`

### Variables no disponibles

1. Verifica que la variable está en `.env` o `config.yml`
2. Revisa la sintaxis YAML si está en `config.yml`
3. Usa `getattr()` con valor por defecto si la variable es opcional

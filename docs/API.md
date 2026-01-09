# Documentación de la API

## Endpoints

### GET `/`

Health check básico del servicio.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### GET `/health`

Verificación del estado del servicio y del modelo.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

Status puede ser:
- `healthy`: Modelo cargado y funcionando
- `degraded`: Modelo no disponible

### POST `/predict`

Realiza una predicción individual de especie de Iris.

**Request:**
```json
{
  "features": {
    "sepal_length_cm": 5.1,
    "sepal_width_cm": 3.5,
    "petal_length_cm": 1.4,
    "petal_width_cm": 0.2
  }
}
```

**Response:**
```json
{
  "predicted_species": "Iris-setosa",
  "probabilities": [
    {
      "species": "Iris-setosa",
      "probability": 0.98
    },
    {
      "species": "Iris-versicolor",
      "probability": 0.01
    },
    {
      "species": "Iris-virginica",
      "probability": 0.01
    }
  ]
}
```

**Errores:**
- `422`: Validación fallida (valores inválidos)
- `503`: Modelo no disponible
- `500`: Error interno del servidor

## Validaciones

### IrisFeatures

- `sepal_length_cm`: float, 0.0 <= valor <= 20.0
- `sepal_width_cm`: float, 0.0 <= valor <= 20.0
- `petal_length_cm`: float, 0.0 <= valor <= 20.0
- `petal_width_cm`: float, 0.0 <= valor <= 20.0

Todos los valores deben ser positivos.

## Documentación Interactiva

La API incluye documentación interactiva:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Ejemplos de Uso

### cURL

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "features": {
         "sepal_length_cm": 5.1,
         "sepal_width_cm": 3.5,
         "petal_length_cm": 1.4,
         "petal_width_cm": 0.2
       }
     }'
```

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "features": {
            "sepal_length_cm": 5.1,
            "sepal_width_cm": 3.5,
            "petal_length_cm": 1.4,
            "petal_width_cm": 0.2
        }
    }
)

print(response.json())
```

### JavaScript

```javascript
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    features: {
      sepal_length_cm: 5.1,
      sepal_width_cm: 3.5,
      petal_length_cm: 1.4,
      petal_width_cm: 0.2
    }
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

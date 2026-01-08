# Guía de Contribución

## Configuración del Entorno de Desarrollo

1. Fork el repositorio
2. Clona tu fork:
```bash
git clone https://github.com/tu-usuario/iris-ml-pipeline.git
cd iris-ml-pipeline
```

3. Instala Poetry si no lo tienes:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

4. Instala las dependencias:
```bash
poetry install
```

5. Activa el entorno virtual:
```bash
poetry shell
```

## Estándares de Código

### PEP 8

El código debe seguir PEP 8. Verifica con:
```bash
poetry run pycodestyle src/ tests/
```

### Type Hints

Todas las funciones deben tener type hints:
```python
def ejemplo(x: int, y: str) -> bool:
    """Función de ejemplo."""
    return True
```

### Docstrings

Usa estilo Google para docstrings:
```python
def ejemplo(x: int, y: str) -> bool:
    """Descripción breve.

    Descripción detallada si es necesario.

    Args:
        x: Descripción del parámetro x.
        y: Descripción del parámetro y.

    Returns:
        Descripción del valor de retorno.

    Raises:
        ValueError: Cuando algo sale mal.
    """
    if x < 0:
        raise ValueError("x debe ser positivo")
    return True
```

### Formateo

Usa Black para formatear el código:
```bash
poetry run black src/ tests/
```

## Testing

### Escribir Pruebas

- Pruebas unitarias: `tests/unit/`
- Pruebas de integración: `tests/integration/`
- Pruebas funcionales: `tests/functional/`

### Ejecutar Pruebas

```bash
# Todas las pruebas
poetry run pytest

# Con cobertura
poetry run pytest --cov=src/iris_ml --cov-report=html
```

### Cobertura

Mantén la cobertura de código por encima del 80%.

## Workflow de Git

1. Crea una rama para tu feature:
```bash
git checkout -b feature/nueva-funcionalidad
```

2. Haz commits descriptivos:
```bash
git commit -m "feat: agregar nueva funcionalidad"
```

3. Push a tu fork:
```bash
git push origin feature/nueva-funcionalidad
```

4. Abre un Pull Request

## Convención de Commits

Usa Conventional Commits:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato de código
- `refactor`: Refactorización
- `test`: Pruebas
- `chore`: Tareas de mantenimiento

## Checklist para Pull Requests

- [ ] El código sigue PEP 8
- [ ] Todas las funciones tienen type hints
- [ ] Todas las funciones tienen docstrings
- [ ] Se agregaron pruebas (unitarias, integración o funcionales)
- [ ] Todas las pruebas pasan
- [ ] La cobertura de código se mantiene o aumenta
- [ ] Se actualizó la documentación si es necesario
- [ ] El código fue formateado con Black

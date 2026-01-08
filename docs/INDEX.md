# Índice de Documentación

## Documentación Principal

- [README](../README.md) - Documentación principal del proyecto
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitectura y diseño del sistema
- [API.md](API.md) - Documentación de la API REST
- [DEVELOPMENT.md](DEVELOPMENT.md) - Guía de desarrollo
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guía para contribuir

## Temas Cubiertos

Este proyecto implementa todos los temas solicitados:

### Estándares de Código

1. **PEP 8 y pycodestyle**: Código formateado según estándares
   - Archivos: Todo el código fuente
   - Verificación: `poetry run pycodestyle src/ tests/`

2. **Python Annotations**: Type hints completos
   - Ejemplo: `src/iris_ml/models/pipeline.py`
   - Verificación: `poetry run mypy src/`

3. **Docstrings**: Documentación estilo Google
   - Ejemplo: Cualquier módulo en `src/iris_ml/`
   - Verificación: `poetry run pydocstyle src/`

4. **Intra-package references**: Referencias correctas entre módulos
   - Ejemplo: `src/iris_ml/config/__init__.py`
   - Ver: PEP 8 para imports relativos/absolutos

### Configuración y Empaquetado

5. **PEP 621**: Metadatos en `pyproject.toml`
   - Archivo: `pyproject.toml`
   - Sección: `[tool.poetry]`

6. **Poetry**: Gestión de dependencias
   - Archivo: `pyproject.toml`
   - Comandos: `poetry install`, `poetry add`, etc.

7. **Dynaconf**: Configuración por entornos
   - Archivos: `settings.toml`, `src/iris_ml/config/settings.py`
   - Entornos: development, testing, production

### Testing

8. **Pruebas unitarias**: Componentes individuales
   - Carpeta: `tests/unit/`
   - Ejecutar: `poetry run pytest tests/unit/`

9. **Pruebas de integración**: Componentes integrados
   - Carpeta: `tests/integration/`
   - Ejecutar: `poetry run pytest tests/integration/`

10. **Pruebas funcionales**: End-to-end
    - Carpeta: `tests/functional/`
    - Ejecutar: `poetry run pytest tests/functional/`

11. **Pytest**: Framework de testing
    - Configuración: `pyproject.toml` → `[tool.pytest.ini_options]`
    - Fixtures: `tests/conftest.py`

### CI/CD

12. **GitHub Actions**: Automatización CI/CD
    - Archivo: `.github/workflows/ci.yml`
    - Jobs: lint, test, build

### Desarrollo y Arquitectura

13. **Refactorización y buenas prácticas**: Código limpio
    - Ver: `docs/ARCHITECTURE.md`
    - Principios: SOLID, DRY, KISS

14. **POO**: Programación orientada a objetos
    - Ejemplo: `src/iris_ml/models/pipeline.py`
    - Clases: `IrisPipeline`, `ColumnSelector`, `SpeciesEncoder`

### API y Validación

15. **REST API**: API REST con FastAPI
    - Archivo: `src/iris_ml/api/main.py`
    - Documentación: `docs/API.md`

16. **Pydantic**: Validación de datos
    - Archivo: `src/iris_ml/api/schemas.py`
    - Uso: Request/Response models

### Machine Learning

17. **Pipelines scikit-learn**: BaseEstimator y TransformerMixin
    - Archivo: `src/iris_ml/preprocessing/transformers.py`
    - Clases: `ColumnSelector`, `SpeciesEncoder`
    - Integración: `src/iris_ml/models/pipeline.py`

## Estructura del Proyecto

```
tec_mon_mod_3_session_13/
├── src/iris_ml/          # Código fuente
├── tests/                # Pruebas
├── docs/                 # Documentación
├── .github/workflows/    # GitHub Actions
├── pyproject.toml        # Configuración Poetry (PEP 621)
├── settings.toml         # Configuración Dynaconf
└── README.md            # Documentación principal
```

## Comandos Rápidos

```bash
# Instalar dependencias
poetry install

# Ejecutar todas las pruebas
poetry run pytest

# Formatear código
poetry run black src/ tests/

# Verificar PEP 8
poetry run pycodestyle src/ tests/

# Entrenar modelo
poetry run iris-train

# Iniciar API
poetry run iris-api
```

## Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Dynaconf Documentation](https://www.dynaconf.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [PEP 8](https://pep8.org/)
- [PEP 621](https://peps.python.org/pep-0621/)

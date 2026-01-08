# Poetry 2.0+ - Cambios Importantes

## Cambios en Poetry 2.0

Desde Poetry 2.0.0, el comando `poetry shell` **ya no está disponible por defecto**.

## Opciones para Activar el Entorno Virtual

### Opción 1: `poetry env activate` (Recomendado)

```bash
poetry env activate
```

Este es el nuevo comando recomendado en Poetry 2.0+.

**Nota**: Este comando es diferente a `poetry shell`:
- No crea una nueva sesión de shell
- Activa el entorno en el shell actual
- Es similar a `source .venv/bin/activate`

### Opción 2: Activar Manualmente (Más Familiar)

```bash
# En macOS/Linux
source .venv/bin/activate

# En Windows
.venv\Scripts\activate
```

Este método funciona igual que siempre y es el más familiar.

### Opción 3: Instalar el Plugin Shell (Retrocompatibilidad)

Si quieres usar `poetry shell` como antes:

```bash
# Instalar el plugin
poetry self add poetry-plugin-shell

# Ahora puedes usar
poetry shell
```

## Opción 4: Usar `poetry run` (Sin Activar)

No necesitas activar el entorno virtual para ejecutar comandos:

```bash
# Ejecutar comandos directamente
poetry run pytest
poetry run python -m iris_ml.train
poetry run iris-train

# Ver la ruta del entorno virtual
poetry env info --path
```

## Recomendación para Estudiantes

Para evitar confusión, recomendamos:

1. **No activar el entorno** y usar `poetry run` para todo:
   ```bash
   poetry run pytest
   poetry run iris-train
   poetry run iris-api
   ```

2. O **activar manualmente** (más familiar):
   ```bash
   source .venv/bin/activate
   pytest
   python -m iris_ml.train
   ```

## Comparación de Métodos

| Método | Poetry 2.0+ | Familiar | Requiere activación |
|--------|-------------|----------|---------------------|
| `poetry shell` | ❌ No disponible | ✅ Sí | ✅ Sí |
| `poetry env activate` | ✅ Sí | ⚠️ Nuevo | ✅ Sí |
| `source .venv/bin/activate` | ✅ Sí | ✅ Sí | ✅ Sí |
| `poetry run` | ✅ Sí | ⚠️ Diferente | ❌ No |

## Resumen

- **Poetry 2.0+**: `poetry shell` no existe por defecto
- **Alternativa moderna**: `poetry env activate`
- **Alternativa familiar**: `source .venv/bin/activate`
- **Sin activar**: `poetry run <comando>`
- **Retrocompatibilidad**: Instalar plugin `poetry-plugin-shell`

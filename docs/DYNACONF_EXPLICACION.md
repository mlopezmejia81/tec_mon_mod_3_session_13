# Explicación: Dynaconf, settings.py y settings

## Conceptos Clave

### 1. **Dynaconf** = La Biblioteca (el paquete)

**Dynaconf es el paquete de Python que instalas:**

```bash
# Se instala con Poetry
poetry add dynaconf

# O con pip
pip install dynaconf
```

**Es una biblioteca externa** que proporciona la clase `Dynaconf`.

---

### 2. **settings.py** = El Archivo Donde USAS Dynaconf

**`settings.py` es TU archivo** donde importas y configuras Dynaconf:

```python
# src/iris_ml/config/settings.py
from dynaconf import Dynaconf  # ← Importas la biblioteca Dynaconf

# Aquí CREAS una instancia de Dynaconf
settings = Dynaconf(
    settings_files=["config.yml"],
    load_dotenv=True,
    dotenv_path=".env",
)
```

**`settings.py` es código que TÚ escribes** para configurar cómo Dynaconf debe leer tus archivos.

---

### 3. **settings** = El Objeto que Creas

**`settings` es el objeto** que creas usando la clase `Dynaconf`:

```python
settings = Dynaconf(...)  # ← Creas una instancia

# Ahora 'settings' es un objeto que contiene toda tu configuración
debug = settings.debug
port = settings.api.port
```

**`settings` es el objeto** que usas en tu código para acceder a la configuración.

---

## Relación Visual

```
┌─────────────────────────────────────────┐
│  Dynaconf (biblioteca instalada)       │
│  └─ Clase: Dynaconf                    │
│     └─ Métodos: load, get, etc.        │
└─────────────────────────────────────────┘
              │
              │ importas
              ▼
┌─────────────────────────────────────────┐
│  settings.py (TU archivo)                │
│  ┌───────────────────────────────────┐ │
│  │ from dynaconf import Dynaconf     │ │
│  │                                    │ │
│  │ settings = Dynaconf(              │ │
│  │     settings_files=["config.yml"],│ │
│  │     load_dotenv=True,             │ │
│  │ )                                 │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
              │
              │ crea
              ▼
┌─────────────────────────────────────────┐
│  settings (objeto)                       │
│  └─ Contiene toda la configuración      │
│     └─ settings.debug                  │
│     └─ settings.api.port               │
└─────────────────────────────────────────┘
              │
              │ usas en
              ▼
┌─────────────────────────────────────────┐
│  Tu código                               │
│  from iris_ml.config import settings    │
│  debug = settings.debug                 │
└─────────────────────────────────────────┘
```

---

## Analogía Simple

### Dynaconf = La Herramienta
- Es como un **destornillador** (la herramienta que compras)

### settings.py = Cómo Usas la Herramienta
- Es como **instrucciones de uso** (cómo usas el destornillador)

### settings = El Resultado
- Es como el **tornillo ajustado** (el resultado de usar el destornillador)

---

## Ejemplo Paso a Paso

### Paso 1: Instalar Dynaconf (la biblioteca)

```bash
poetry add dynaconf
```

Esto instala el paquete `dynaconf` en tu entorno virtual.

---

### Paso 2: Crear settings.py (tu archivo)

```python
# src/iris_ml/config/settings.py
from dynaconf import Dynaconf  # ← Importas la biblioteca

# Creas una instancia de Dynaconf
settings = Dynaconf(
    settings_files=["config.yml"],
    load_dotenv=True,
    dotenv_path=".env",
)
```

**Este es TU código** que configura cómo Dynaconf debe funcionar.

---

### Paso 3: Usar settings (el objeto)

```python
# En cualquier parte de tu código
from iris_ml.config import settings  # ← Importas el objeto 'settings'

# Usas el objeto
debug = settings.debug
port = settings.api.port
```

**`settings` es el objeto** que contiene toda tu configuración unificada.

---

## Resumen

| Concepto | ¿Qué es? | Ejemplo |
|----------|----------|---------|
| **Dynaconf** | Biblioteca/Paquete de Python | `pip install dynaconf` |
| **settings.py** | Tu archivo donde configuras Dynaconf | `src/iris_ml/config/settings.py` |
| **settings** | El objeto que creas y usas | `settings = Dynaconf(...)` |

---

## Preguntas Frecuentes

### ¿Dynaconf es settings.py?
**No.** Dynaconf es la biblioteca. `settings.py` es donde la usas.

### ¿settings es Dynaconf?
**No exactamente.** `settings` es una **instancia** de la clase `Dynaconf`.

### ¿Puedo tener múltiples objetos settings?
**Sí**, puedes crear múltiples instancias:

```python
# settings.py
from dynaconf import Dynaconf

# Primera instancia
app_settings = Dynaconf(settings_files=["config.yml"])

# Segunda instancia (diferente configuración)
db_settings = Dynaconf(settings_files=["db_config.yml"])
```

### ¿Por qué se llama "settings"?
Es solo una **convención de nombre**. Podrías llamarlo como quieras:

```python
# También válido
config = Dynaconf(...)
my_config = Dynaconf(...)
app_config = Dynaconf(...)
```

Pero `settings` es el nombre más común y claro.

---

## En Este Proyecto

```python
# src/iris_ml/config/settings.py

# 1. Importas la biblioteca Dynaconf
from dynaconf import Dynaconf

# 2. Creas una instancia llamada 'settings'
settings = Dynaconf(
    settings_files=["config.yml", "settings.toml"],
    load_dotenv=True,
    dotenv_path=".env",
)

# 3. Exportas el objeto 'settings'
# (en __init__.py)
```

Luego en tu código:

```python
# Importas el objeto 'settings' que creaste
from iris_ml.config import settings

# Usas el objeto
debug = settings.debug
```

---

## Conclusión

- **Dynaconf** = La biblioteca (herramienta)
- **settings.py** = Tu archivo (cómo usas la herramienta)
- **settings** = El objeto (resultado que usas)

**No son lo mismo, pero trabajan juntos:**
1. Instalas Dynaconf (biblioteca)
2. Escribes settings.py (configuración)
3. Usas settings (objeto)

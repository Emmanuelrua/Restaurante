# 🏗️ Arquitectura

Esta sección describe las decisiones de diseño tomadas en el proyecto y los principios de código limpio aplicados.

---

## Estructura del proyecto (src layout)

El proyecto utiliza el patrón **src layout**, que separa el código fuente de la configuración y los tests:

```
restaurante-cli/
├── main.py                      # Punto de entrada (carga .env antes de importar)
├── pyproject.toml               # Configuración del proyecto
├── schema.sql                   # DDL completo para crear las tablas en Supabase
├── .env                         # Variables de entorno (no se sube a git)
├── data/                        # Archivos JSON de persistencia local
│   ├── meseros.json
│   └── platillos.json
├── src/
│   └── mi_app/
│       ├── cli/                 # Capa de presentación (Typer + Rich)
│       │   ├── app.py
│       │   ├── meseros.py
│       │   └── platillos.py
│       ├── models/              # Entidades del dominio (dataclasses)
│       │   ├── mesero.py
│       │   └── platillo.py
│       ├── services.py          # Lógica de negocio
│       ├── storage.py           # Storage JSON (implementación local)
│       ├── storage_supabase.py  # Storage Supabase (implementación en la nube)
│       └── exceptions.py        # Excepciones personalizadas
├── tests/
│   └── test_services.py
└── docs/                        # Documentación MkDocs
```

!!! info "¿Por qué src layout?"
    Este patrón evita que el código fuente se importe accidentalmente desde la raíz del proyecto, obligando a usar instalaciones explícitas. Es una práctica recomendada por la comunidad Python.

---

## Separación por capas

El sistema está organizado en **4 capas** con responsabilidades bien definidas.  
La capa de Storage tiene dos implementaciones concretas que los servicios **no distinguen**:

```mermaid
flowchart TD
    subgraph Presentación
        CLI["cli/ — Typer + Rich"]
    end

    subgraph Negocio
        SVC["services.py — Lógica de negocio"]
        EXC["exceptions.py — Errores del dominio"]
    end

    subgraph Dominio
        MOD["models/ — Dataclasses"]
    end

    subgraph Persistencia
        PROTO["storage Protocol — contrato abstracto"]
        JSON["MeseroJSONStorage\nPlatilloJSONStorage"]
        SB["MeseroSupabaseStorage\nPlatilloSupabaseStorage"]
    end

    CLI --> SVC
    SVC --> MOD
    SVC --> PROTO
    SVC --> EXC
    PROTO --> JSON
    PROTO --> SB
```

### Capa CLI (`cli/`)

Maneja toda la interacción con el usuario: prompts, tablas Rich, paneles de éxito/error. **No contiene lógica de negocio**; delega todo al servicio correspondiente.  
Al iniciar, decide qué implementación de Storage usar: si las variables `SUPABASE_URL` y `SUPABASE_KEY` están definidas en el entorno, instancia el storage de Supabase; de lo contrario, usa JSON local.

### Capa de Servicios (`services.py`)

Contiene las reglas de negocio: verificar duplicados, buscar por ID, validar credenciales. Recibe un objeto `Storage` por inyección en el constructor y **no sabe** si está hablando con archivos JSON o con Supabase.

### Capa de Modelos (`models/`)

Define las entidades `Mesero` y `Platillo` como `dataclasses` con validaciones en `__post_init__`. Cada entidad vive en su propio archivo.

### Capa de Storage (`storage.py` / `storage_supabase.py`)

Implementa la lectura/escritura de datos.  
Usa `Protocol` para definir el contrato y permite intercambiar implementaciones sin tocar los servicios.

| Implementación | Mecanismo | Cuándo se usa |
|----------------|-----------|---------------|
| `MeseroJSONStorage` | Archivo `data/meseros.json` | Sin `.env` configurado |
| `MeseroSupabaseStorage` | API REST de Supabase (PostgREST) | Con `SUPABASE_URL` y `SUPABASE_KEY` en `.env` |
| `PlatilloJSONStorage` | Archivo `data/platillos.json` | Sin `.env` configurado |
| `PlatilloSupabaseStorage` | API REST de Supabase (PostgREST) | Con `SUPABASE_URL` y `SUPABASE_KEY` en `.env` |

---

## Principios de código limpio aplicados

### Single Responsibility Principle (SRP)

Cada módulo tiene una única responsabilidad:

- `models/` → solo define la estructura y validación de datos.
- `services.py` → solo contiene lógica de negocio.
- `storage.py` / `storage_supabase.py` → solo manejan persistencia.
- `cli/` → solo maneja la interfaz de usuario.

### Dependency Inversion

Los servicios dependen de abstracciones (`Protocol`), no de implementaciones concretas. Esto permite usar mocks en los tests y cambiar el backend de almacenamiento sin tocar la lógica de negocio.

### Open/Closed Principle

El sistema está **abierto para extensión** (se puede agregar `MeseroSQLiteStorage`, `MeseroRedisStorage`, etc.) **sin modificar** los servicios existentes — solo hay que respetar el `Protocol`.

### Don't Repeat Yourself (DRY)

Los helpers de UI (`_ok`, `_error`, `_tabla_meseros`, `_tabla_platillos`) encapsulan patrones repetidos de presentación, evitando duplicar código de Rich en cada comando.  
En `storage_supabase.py`, `_base()`, `_headers()` y `_check()` centralizan la configuración HTTP para evitar repetición entre las dos clases de storage.

### Fail Fast

Los modelos validan sus datos inmediatamente al crearse gracias a `__post_init__`. Si un dato es inválido, se lanza una excepción antes de que el objeto entre en el sistema.

!!! example "Ejemplo de validación temprana"
    ```python
    @dataclass
    class Mesero:
        mesero_id: int
        nombre: str
        pin: str

        def __post_init__(self) -> None:
            self._validar_id()
            self._validar_nombre()
            self._validar_pin()
    ```

---

## Jerarquía de excepciones

Las excepciones siguen una jerarquía que facilita el manejo de errores:

```mermaid
classDiagram
    AppError <|-- MeseroError
    AppError <|-- PlatilloError
    MeseroError <|-- MeseroNoEncontradoError
    MeseroError <|-- MeseroYaExisteError
    MeseroError <|-- DatosMeseroInvalidosError
    PlatilloError <|-- PlatilloNoEncontradoError
    PlatilloError <|-- PlatilloYaExisteError
    PlatilloError <|-- DatosPlatilloInvalidosError
    PlatilloError <|-- CategoriaInvalidaError
```

!!! tip "¿Por qué una jerarquía?"
    Permite capturar errores de forma granular (`MeseroNoEncontradoError`) o general (`AppError`) según el contexto.

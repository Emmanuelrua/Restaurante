# 🚀 Primeros pasos

Esta guía te ayudará a instalar y ejecutar el proyecto en tu máquina local.

## Requisitos previos

- **Python 3.12** o superior
- **uv** — gestor de paquetes y entornos virtuales

!!! info "¿No tienes uv instalado?"
    Puedes instalarlo siguiendo las instrucciones oficiales en [docs.astral.sh/uv](https://docs.astral.sh/uv/).

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/restaurante-cli.git
cd restaurante-cli
```

### 2. Instalar dependencias

=== "MacOS / Linux"

    ```bash
    uv sync
    ```

=== "Windows"

    ```bash
    uv sync
    ```

Esto creará el entorno virtual y descargará todas las dependencias definidas en `pyproject.toml`.

## Primer comando

Para verificar que todo funciona correctamente, ejecuta:

```bash
uv run python main.py --help
```

Deberías ver la ayuda del CLI con los subcomandos disponibles:

```
 Usage: main.py [OPTIONS] COMMAND [ARGS]...

 🍽️  Sistema de gestión del restaurante

╭─ Commands ──────────────────────────────╮
│ menu        Abre el menú interactivo    │
│ meseros     👤  Gestión de meseros       │
│ platillos   🍲  Gestión del menú         │
╰─────────────────────────────────────────╯
```

## Abrir el menú interactivo

```bash
uv run python main.py menu
```

!!! success "¡Listo!"
    Si ves el menú principal con las opciones de meseros y platillos, el proyecto está correctamente instalado.

## Ejecutar los tests

```bash
uv run pytest -v
```

## Verificar calidad del código

=== "Lint"

    ```bash
    uv run ruff check .
    ```

=== "Complejidad ciclomática"

    ```bash
    uv run radon cc src -a
    ```

!!! warning "Complejidad"
    El proyecto debe mantener una calificación promedio de **A** en complejidad ciclomática.

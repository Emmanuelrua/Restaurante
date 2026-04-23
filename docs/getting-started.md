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
    Por defecto los datos se guardan en `data/meseros.json` y `data/platillos.json`.

---

## Configurar Supabase (opcional)

Si quieres persistir los datos en la nube usando **Supabase + PostgreSQL**, sigue estos pasos adicionales:

### 1. Crear las tablas en Supabase

En el panel de Supabase, ve a **SQL Editor** y ejecuta el contenido completo de `schema.sql` (incluido en la raíz del proyecto). Esto creará las tablas `meseros`, `platillos`, `mesas`, `pedidos` y `detalle_pedido` con todos sus datos de prueba.

### 2. Configurar las credenciales

Edita el archivo `.env` en la raíz del proyecto y completa tus credenciales:

```bash
# .env
SUPABASE_URL=https://[TU_REF].supabase.co
SUPABASE_KEY=[TU_ANON_KEY_O_SERVICE_ROLE_KEY]
```

Puedes encontrar estos valores en **Supabase → Settings → API**.

!!! warning "Seguridad"
    El archivo `.env` está incluido en `.gitignore` y **nunca debe subirse al repositorio**.  
    Nunca compartas tu `service_role key` de forma pública.

### 3. Ejecutar con Supabase

Simplemente ejecuta la aplicación normalmente; detectará las credenciales automáticamente:

```bash
uv run python main.py menu
```

!!! info "¿Cómo sé qué backend está activo?"
    Si `SUPABASE_URL` y `SUPABASE_KEY` están definidos en `.env`, la app usa Supabase.  
    Si no están, usa los archivos JSON locales. No hay ningún flag adicional que cambiar.

---

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

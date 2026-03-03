# 🍽️ Mesa & Co — Sistema de gestión para restaurante

Aplicación de terminal (CLI) para gestionar el personal de meseros y el menú de platillos de un restaurante. Construida con Python, Typer y Rich, siguiendo una arquitectura limpia de capas separadas.

## 📋 Alcance

- Registro y autenticación de meseros con PIN de 4 dígitos.
- CRUD completo de platillos organizados por categorías.
- Categorías disponibles: `entrada`, `plato_fuerte`, `postre`, `bebida`.
- Dos archivos JSON independientes como base de datos local (`meseros.json`, `platillos.json`).
- Interfaz interactiva con menú numerado **y** comandos directos por flags.

---

## 🏗️ Estructura del proyecto

```
restaurante-cli/
├── .github/workflows/tests.yml   # CI: lint + tests automáticos
├── data/
│   ├── meseros.json              # Base de datos de meseros
│   └── platillos.json            # Base de datos de platillos
├── main.py                       # Punto de entrada
├── src/mi_app/
│   ├── models.py                 # Dataclasses: Mesero, Platillo
│   ├── services.py               # Lógica de negocio y validaciones
│   ├── storage.py                # Lectura/escritura JSON
│   ├── exceptions.py             # Excepciones personalizadas
│   └── cli/
│       ├── app.py                # Menú interactivo principal
│       ├── meseros.py            # Comandos y flujos de meseros
│       └── platillos.py          # Comandos y flujos de platillos
└── tests/test_services.py        # 14 casos de prueba con pytest
```

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/restaurante-cli.git
cd restaurante-cli

# Instalar dependencias con uv
uv sync
```

---

## 💻 Uso

### Opción A — Menú interactivo

La forma principal de usar la app. Muestra un menú numerado y pide los datos campo a campo:

```bash
uv run python main.py menu
```

Al ejecutarlo verás:

```
┌────────┬────────────────────────────────┐
│── MESEROS ──                            │
│   1    │ Registrar mesero               │
│   2    │ Login de mesero                │
│   3    │ Listar meseros                 │
│   4    │ Buscar mesero por ID           │
│   5    │ Eliminar mesero                │
│── PLATILLOS ──                          │
│   6    │ Agregar platillo               │
│   7    │ Ver menú completo              │
│   8    │ Filtrar por categoría          │
│   9    │ Buscar platillo por ID         │
│  10    │ Actualizar platillo            │
│  11    │ Eliminar platillo              │
│   0    │ Salir                          │
└────────┴────────────────────────────────┘
```

Cada opción guía al usuario con prompts interactivos. El PIN se oculta al escribirlo. Las categorías se eligen por número.

---

### Opción B — Comandos directos (flags)

También se puede operar sin el menú, pasando los datos directamente:

#### Meseros

```bash
# Registrar
uv run python main.py meseros registrar --id 1 --nombre "Carlos Pérez" --pin 1234

# Login
uv run python main.py meseros login --id 1 --pin 1234

# Listar todos
uv run python main.py meseros listar

# Buscar por ID
uv run python main.py meseros obtener --id 1

# Eliminar
uv run python main.py meseros eliminar --id 1
```

#### Platillos

```bash
# Crear
uv run python main.py platillos crear --id 1 --nombre "Sopa del día" --precio 12000 --categoria entrada

# Listar todos
uv run python main.py platillos listar

# Listar por categoría
uv run python main.py platillos listar --categoria plato_fuerte

# Buscar por ID
uv run python main.py platillos obtener --id 1

# Actualizar
uv run python main.py platillos actualizar --id 1 --nombre "Sopa de tomate" --precio 13000 --categoria entrada

# Eliminar
uv run python main.py platillos eliminar --id 1
```

#### Categorías válidas

| Categoría      | Emoji | Descripción        |
|----------------|-------|--------------------|
| `entrada`      | 🥗    | Sopas, ensaladas   |
| `plato_fuerte` | 🍖    | Platos principales |
| `postre`       | 🍮    | Dulces, helados    |
| `bebida`       | 🥤    | Jugos, gaseosas    |

---

## 🧪 Testing

```bash
# Correr todos los tests
uv run pytest

# Con detalle de cada caso
uv run pytest -v
```

El proyecto incluye 14 casos de prueba que cubren escenarios exitosos, duplicados, no encontrados y datos inválidos para ambas entidades.

---

## 🔍 Lint

```bash
uv run ruff check .
```

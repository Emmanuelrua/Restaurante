# 🖥️ Comandos CLI

Restaurante CLI ofrece dos formas de interacción: un **menú interactivo** y **comandos directos** con flags.

---

## Menú interactivo

```bash
uv run python main.py menu
```

Abre una interfaz en la terminal donde puedes navegar entre opciones usando números.

!!! tip "Recomendado para uso rápido"
    El menú interactivo solicita todos los datos paso a paso con prompts.

---

## Comandos de Meseros

### Registrar un mesero

=== "Menú interactivo"

    Selecciona la opción **1** y sigue los prompts.

=== "Comando directo"

    ```bash
    uv run python main.py meseros registrar --id 1 --nombre "Carlos Pérez" --pin 1234
    ```

**Parámetros:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `--id` | `int` | ID único del mesero |
| `--nombre` | `str` | Nombre completo |
| `--pin` | `str` | PIN de 4 dígitos numéricos |

**Ejemplo de salida:**

```
╭──────────────────────────────────────────╮
│ ✅ Mesero Carlos Pérez registrado con ID 1│
╰──────────────────────────────────────────╯
```

---

### Login de mesero

=== "Menú interactivo"

    Selecciona la opción **2**.

=== "Comando directo"

    ```bash
    uv run python main.py meseros login --id 1 --pin 1234
    ```

---

### Listar meseros

```bash
uv run python main.py meseros listar
```

Muestra una tabla con todos los meseros registrados. El PIN se muestra oculto con `●●●●`.

---

### Buscar mesero por ID

```bash
uv run python main.py meseros obtener --id 1
```

---

### Eliminar mesero

```bash
uv run python main.py meseros eliminar --id 1
```

!!! danger "Acción irreversible"
    Una vez eliminado, el mesero no puede recuperarse.

---

## Comandos de Platillos

### Crear un platillo

=== "Menú interactivo"

    Selecciona la opción **6** y sigue los prompts.

=== "Comando directo"

    ```bash
    uv run python main.py platillos crear --id 1 --nombre "Sopa del día" --precio 12000 --categoria entrada
    ```

**Parámetros:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `--id` | `int` | ID único del platillo |
| `--nombre` | `str` | Nombre del platillo |
| `--precio` | `float` | Precio en pesos colombianos |
| `--categoria` | `str` | `entrada`, `plato_fuerte`, `postre` o `bebida` |

---

### Listar menú completo

```bash
uv run python main.py platillos listar
```

### Filtrar por categoría

```bash
uv run python main.py platillos listar --categoria entrada
```

---

### Buscar platillo por ID

```bash
uv run python main.py platillos obtener --id 1
```

---

### Actualizar platillo

```bash
uv run python main.py platillos actualizar --id 1 --nombre "Sopa criolla" --precio 15000 --categoria entrada
```

---

### Eliminar platillo

```bash
uv run python main.py platillos eliminar --id 1
```

!!! danger "Acción irreversible"
    El platillo se eliminará permanentemente del menú.

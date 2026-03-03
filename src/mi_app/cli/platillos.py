from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.mi_app.exceptions import AppError
from src.mi_app.models import Platillo
from src.mi_app.services import PlatilloService
from src.mi_app.storage import PlatilloJSONStorage

app = typer.Typer(no_args_is_help=True)
console = Console()

service = PlatilloService(PlatilloJSONStorage(Path("data/platillos.json")))

CATEGORIA_ESTILOS: dict[str, tuple[str, str]] = {
    "entrada": ("🥗", "green"),
    "plato_fuerte": ("🍖", "yellow"),
    "postre": ("🍮", "magenta"),
    "bebida": ("🥤", "blue"),
}

CATEGORIAS_VALIDAS = list(CATEGORIA_ESTILOS.keys())


# ── Helpers de UI ─────────────────────────────────────────────────────────────


def _icono_categoria(categoria: str) -> str:
    """Retorna el emoji correspondiente a la categoría."""
    return CATEGORIA_ESTILOS.get(categoria, ("🍽️", "white"))[0]


def _color_categoria(categoria: str) -> str:
    """Retorna el color Rich correspondiente a la categoría."""
    return CATEGORIA_ESTILOS.get(categoria, ("🍽️", "white"))[1]


def _tabla_platillos(platillos: list[Platillo], titulo: str = "🍽️  Menú del restaurante") -> Table:
    """Construye y retorna una tabla Rich con la lista de platillos."""
    tabla = Table(
        title=titulo,
        title_style="bold magenta",
        border_style="magenta",
        header_style="bold white on dark_magenta",
        show_lines=True,
    )
    tabla.add_column("ID", justify="center", style="bright_cyan", width=6)
    tabla.add_column("Nombre", style="white", min_width=22)
    tabla.add_column("Precio", justify="right", style="bright_green", width=14)
    tabla.add_column("Categoría", justify="center", min_width=16)
    tabla.add_column("Disponible", justify="center", width=12)

    for p in platillos:
        icono = _icono_categoria(p.categoria)
        color = _color_categoria(p.categoria)
        disponible = "[green]✅ Sí[/green]" if p.disponible else "[red]❌ No[/red]"
        tabla.add_row(
            str(p.platillo_id),
            p.nombre,
            f"$ {p.precio:,.0f}",
            f"[{color}]{icono} {p.categoria}[/{color}]",
            disponible,
        )

    return tabla


def _ok(mensaje: str) -> None:
    """Imprime un mensaje de éxito con panel verde."""
    console.print(Panel(f"[bold green]✅ {mensaje}[/bold green]", border_style="green"))


def _error(mensaje: str) -> None:
    """Imprime un mensaje de error con panel rojo."""
    console.print(Panel(f"[bold red]❌ {mensaje}[/bold red]", border_style="red"))


def _pedir_categoria() -> str:
    """Muestra las categorías disponibles y pide al usuario que elija una."""
    console.print("\n  Categorías disponibles:")
    for i, cat in enumerate(CATEGORIAS_VALIDAS, 1):
        icono = _icono_categoria(cat)
        color = _color_categoria(cat)
        console.print(f"    [{color}]{i}. {icono} {cat}[/{color}]")
    opcion = typer.prompt("  Elige una categoría (número)", type=int)
    if opcion < 1 or opcion > len(CATEGORIAS_VALIDAS):
        raise typer.BadParameter("Opción fuera de rango")
    return CATEGORIAS_VALIDAS[opcion - 1]


# ── Flujos interactivos (reutilizables desde el menú) ─────────────────────────


def flujo_crear() -> None:
    """Pide los datos por prompt y crea un platillo."""
    console.print("\n[bold magenta]── Agregar platillo ──[/bold magenta]")
    platillo_id = typer.prompt("  ID del platillo", type=int)
    nombre = typer.prompt("  Nombre del platillo")
    precio = typer.prompt("  Precio (COP)", type=float)
    categoria = _pedir_categoria()
    try:
        platillo = Platillo(
            platillo_id=platillo_id, nombre=nombre, precio=precio, categoria=categoria
        )
        service.crear_platillo(platillo)
        _ok(f"Platillo [bold magenta]{nombre}[/bold magenta] agregado al menú")
    except AppError as e:
        _error(str(e))


def flujo_listar() -> None:
    """Muestra la tabla completa del menú."""
    platillos = service.listar_platillos()
    if not platillos:
        console.print(Panel("[yellow]No hay platillos en el menú.[/yellow]", border_style="yellow"))
        return
    console.print()
    console.print(_tabla_platillos(platillos))
    console.print(f"\n[dim]Total: {len(platillos)} platillo(s)[/dim]")


def flujo_listar_categoria() -> None:
    """Pide una categoría y muestra solo esos platillos."""
    console.print("\n[bold magenta]── Filtrar por categoría ──[/bold magenta]")
    categoria = _pedir_categoria()
    platillos = service.listar_por_categoria(categoria)
    if not platillos:
        console.print(
            Panel(f"[yellow]No hay platillos en '{categoria}'.[/yellow]", border_style="yellow")
        )
        return
    console.print()
    console.print(_tabla_platillos(platillos, f"🍽️  Menú — {categoria}"))
    console.print(f"\n[dim]Total: {len(platillos)} platillo(s)[/dim]")


def flujo_obtener() -> None:
    """Pide un ID y muestra el detalle del platillo."""
    console.print("\n[bold magenta]── Buscar platillo ──[/bold magenta]")
    platillo_id = typer.prompt("  ID del platillo", type=int)
    try:
        p = service.obtener_platillo(platillo_id)
        icono = _icono_categoria(p.categoria)
        color = _color_categoria(p.categoria)
        console.print()
        console.print(
            Panel(
                f"[bold magenta]ID:[/bold magenta]         {p.platillo_id}\n"
                f"[bold magenta]Nombre:[/bold magenta]     {p.nombre}\n"
                f"[bold magenta]Precio:[/bold magenta]     $ {p.precio:,.0f}\n"
                f"[bold magenta]Categoría:[/bold magenta]  [{color}]{icono} {p.categoria}"
                f"[/{color}]\n"
                f"[bold magenta]Disponible:[/bold magenta] "
                f"{'[green]✅ Sí[/green]' if p.disponible else '[red]❌ No[/red]'}",
                title="[bold]Detalle del platillo[/bold]",
                border_style="magenta",
            )
        )
    except AppError as e:
        _error(str(e))


def flujo_actualizar() -> None:
    """Pide los datos por prompt y actualiza un platillo existente."""
    console.print("\n[bold magenta]── Actualizar platillo ──[/bold magenta]")
    platillo_id = typer.prompt("  ID del platillo a actualizar", type=int)
    nombre = typer.prompt("  Nuevo nombre")
    precio = typer.prompt("  Nuevo precio (COP)", type=float)
    categoria = _pedir_categoria()
    try:
        service.actualizar_platillo(platillo_id, nombre, precio, categoria)
        _ok(f"Platillo ID [bold cyan]{platillo_id}[/bold cyan] actualizado correctamente")
    except AppError as e:
        _error(str(e))


def flujo_eliminar() -> None:
    """Pide un ID y elimina el platillo."""
    console.print("\n[bold magenta]── Eliminar platillo ──[/bold magenta]")
    platillo_id = typer.prompt("  ID del platillo a eliminar", type=int)
    try:
        service.eliminar_platillo(platillo_id)
        _ok(f"Platillo ID [bold cyan]{platillo_id}[/bold cyan] eliminado del menú")
    except AppError as e:
        _error(str(e))


# ── Comandos Typer (--flags) ──────────────────────────────────────────────────


@app.command("crear")
def crear(
    platillo_id: int = typer.Option(..., "--id", help="ID único del platillo"),
    nombre: str = typer.Option(..., "--nombre", help="Nombre del platillo"),
    precio: float = typer.Option(..., "--precio", help="Precio en pesos colombianos"),
    categoria: str = typer.Option(
        ..., "--categoria", help="entrada | plato_fuerte | postre | bebida"
    ),
) -> None:
    """Agrega un nuevo platillo al menú."""
    try:
        platillo = Platillo(
            platillo_id=platillo_id, nombre=nombre, precio=precio, categoria=categoria
        )
        service.crear_platillo(platillo)
        _ok(f"Platillo [bold magenta]{nombre}[/bold magenta] agregado al menú")
    except AppError as e:
        _error(str(e))
        raise typer.Exit(code=1)


@app.command("listar")
def listar(
    categoria: str = typer.Option("", "--categoria", help="Filtrar por categoría (opcional)"),
) -> None:
    """Muestra todos los platillos del menú, opcionalmente filtrados por categoría."""
    platillos = service.listar_por_categoria(categoria) if categoria else service.listar_platillos()
    if not platillos:
        console.print(Panel("[yellow]No hay platillos en el menú.[/yellow]", border_style="yellow"))
        return
    titulo = f"🍽️  Menú — {categoria}" if categoria else "🍽️  Menú completo del restaurante"
    console.print()
    console.print(_tabla_platillos(platillos, titulo))
    console.print(f"\n[dim]Total: {len(platillos)} platillo(s)[/dim]")


@app.command("obtener")
def obtener(
    platillo_id: int = typer.Option(..., "--id", help="ID del platillo a buscar"),
) -> None:
    """Muestra el detalle de un platillo específico."""
    try:
        p = service.obtener_platillo(platillo_id)
        icono = _icono_categoria(p.categoria)
        color = _color_categoria(p.categoria)
        console.print()
        console.print(
            Panel(
                f"[bold magenta]ID:[/bold magenta]         {p.platillo_id}\n"
                f"[bold magenta]Nombre:[/bold magenta]     {p.nombre}\n"
                f"[bold magenta]Precio:[/bold magenta]     $ {p.precio:,.0f}\n"
                f"[bold magenta]Categoría:[/bold magenta]  [{color}]{icono} {p.categoria}"
                f"[/{color}]\n"
                f"[bold magenta]Disponible:[/bold magenta] "
                f"{'[green]✅ Sí[/green]' if p.disponible else '[red]❌ No[/red]'}",
                title="[bold]Detalle del platillo[/bold]",
                border_style="magenta",
            )
        )
    except AppError as e:
        _error(str(e))
        raise typer.Exit(code=1)


@app.command("actualizar")
def actualizar(
    platillo_id: int = typer.Option(..., "--id", help="ID del platillo a actualizar"),
    nombre: str = typer.Option(..., "--nombre", help="Nuevo nombre"),
    precio: float = typer.Option(..., "--precio", help="Nuevo precio"),
    categoria: str = typer.Option(..., "--categoria", help="Nueva categoría"),
) -> None:
    """Actualiza los datos de un platillo existente."""
    try:
        service.actualizar_platillo(platillo_id, nombre, precio, categoria)
        _ok(f"Platillo ID [bold cyan]{platillo_id}[/bold cyan] actualizado correctamente")
    except AppError as e:
        _error(str(e))
        raise typer.Exit(code=1)


@app.command("eliminar")
def eliminar(
    platillo_id: int = typer.Option(..., "--id", help="ID del platillo a eliminar"),
) -> None:
    """Elimina un platillo del menú por su ID."""
    try:
        service.eliminar_platillo(platillo_id)
        _ok(f"Platillo ID [bold cyan]{platillo_id}[/bold cyan] eliminado del menú")
    except AppError as e:
        _error(str(e))
        raise typer.Exit(code=1)

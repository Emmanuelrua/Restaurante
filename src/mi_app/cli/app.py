import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .meseros import app as meseros_app
from .meseros import flujo_eliminar as eliminar_mesero
from .meseros import flujo_listar as listar_meseros
from .meseros import flujo_login, flujo_registrar
from .meseros import flujo_obtener as obtener_mesero
from .platillos import app as platillos_app
from .platillos import flujo_actualizar, flujo_crear, flujo_listar_categoria
from .platillos import flujo_eliminar as eliminar_platillo
from .platillos import flujo_listar as listar_platillos
from .platillos import flujo_obtener as obtener_platillo

app = typer.Typer(
    help="🍽️  Sistema de gestión del restaurante",
    no_args_is_help=True,
)

app.add_typer(meseros_app, name="meseros", help="👤  Gestión de meseros")
app.add_typer(platillos_app, name="platillos", help="🍲  Gestión del menú")

console = Console()

# ── Opciones del menú ─────────────────────────────────────────────────────────

OPCIONES_MESEROS: list[tuple[str, str]] = [
    ("1", "Registrar mesero"),
    ("2", "Login de mesero"),
    ("3", "Listar meseros"),
    ("4", "Buscar mesero por ID"),
    ("5", "Eliminar mesero"),
]

OPCIONES_PLATILLOS: list[tuple[str, str]] = [
    ("6", "Agregar platillo"),
    ("7", "Ver menú completo"),
    ("8", "Filtrar por categoría"),
    ("9", "Buscar platillo por ID"),
    ("10", "Actualizar platillo"),
    ("11", "Eliminar platillo"),
]

ACCIONES: dict[str, object] = {
    "1": flujo_registrar,
    "2": flujo_login,
    "3": listar_meseros,
    "4": obtener_mesero,
    "5": eliminar_mesero,
    "6": flujo_crear,
    "7": listar_platillos,
    "8": flujo_listar_categoria,
    "9": obtener_platillo,
    "10": flujo_actualizar,
    "11": eliminar_platillo,
}


# ── Helpers del menú ──────────────────────────────────────────────────────────


def _imprimir_menu() -> None:
    """Imprime el menú principal con las dos secciones."""
    tabla = Table(
        title="🍽️  Restaurante — Menú principal",
        title_style="bold white",
        border_style="bright_white",
        header_style="bold white on grey23",
        show_lines=True,
        min_width=44,
    )
    tabla.add_column("Opción", justify="center", style="bold bright_cyan", width=8)
    tabla.add_column("Acción", style="white", min_width=28)

    tabla.add_row("[bold cyan]── MESEROS ──[/bold cyan]", "", end_section=False)
    for num, desc in OPCIONES_MESEROS:
        tabla.add_row(num, desc)

    tabla.add_row("[bold magenta]── PLATILLOS ──[/bold magenta]", "", end_section=False)
    for num, desc in OPCIONES_PLATILLOS:
        tabla.add_row(num, desc)

    tabla.add_row("[bold red]0[/bold red]", "[dim]Salir[/dim]")

    console.print()
    console.print(tabla)


# ── Comando menú ──────────────────────────────────────────────────────────────


@app.command("menu")
def menu() -> None:
    """Abre el menú interactivo principal del restaurante."""
    console.print(
        Panel(
            "[bold white]Bienvenido al sistema de gestión[/bold white]",
            border_style="bright_white",
        )
    )

    while True:
        _imprimir_menu()
        opcion = typer.prompt("\n  Elige una opción").strip()

        if opcion == "0":
            console.print(Panel("[dim]👋 Hasta luego[/dim]", border_style="dim"))
            raise typer.Exit()

        accion = ACCIONES.get(opcion)
        if accion is None:
            console.print(
                Panel("[red]Opción no válida. Intenta de nuevo.[/red]", border_style="red")
            )
            continue

        accion()  # type: ignore[operator]
        typer.prompt("\n  Presiona Enter para continuar", default="", show_default=False)
        console.clear()

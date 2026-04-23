import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.mi_app.exceptions import AppError
from src.mi_app.models import Mesero
from src.mi_app.services import MeseroService
from src.mi_app.storage_supabase import MeseroSupabaseStorage

app = typer.Typer(no_args_is_help=True)
console = Console()

service = MeseroService(MeseroSupabaseStorage())


# ── Helpers de UI ─────────────────────────────────────────────────────────────


def _tabla_meseros(meseros: list[Mesero], titulo: str = "👤 Meseros registrados") -> Table:
    """Construye y retorna una tabla Rich con la lista de meseros."""
    tabla = Table(
        title=titulo,
        title_style="bold cyan",
        border_style="cyan",
        header_style="bold white on dark_cyan",
        show_lines=True,
    )
    tabla.add_column("ID", justify="center", style="bright_cyan", width=6)
    tabla.add_column("Nombre", style="white", min_width=20)
    tabla.add_column("PIN", justify="center", style="dim white", width=8)

    for m in meseros:
        pin_oculto = "●" * len(m.pin)
        tabla.add_row(str(m.mesero_id), m.nombre, pin_oculto)

    return tabla


def _ok(mensaje: str) -> None:
    """Imprime un mensaje de éxito con panel verde."""
    console.print(Panel(f"[bold green]✅ {mensaje}[/bold green]", border_style="green"))


def _error(mensaje: str) -> None:
    """Imprime un mensaje de error con panel rojo."""
    console.print(Panel(f"[bold red]❌ {mensaje}[/bold red]", border_style="red"))


# ── Flujos interactivos (reutilizables desde el menú) ─────────────────────────


def flujo_registrar() -> None:
    """Pide los datos por prompt y registra un mesero."""
    console.print("\n[bold cyan]── Registrar mesero ──[/bold cyan]")
    nombre = typer.prompt("  Nombre completo")
    pin = typer.prompt("  PIN (4 dígitos)", hide_input=True)
    try:
        mesero = Mesero(nombre=nombre, pin=pin)
        service.registrar_mesero(mesero)
        _ok(f"Mesero [bold cyan]{nombre}[/bold cyan] registrado con ID {mesero.mesero_id}")
    except AppError as e:
        _error(str(e))


def flujo_login() -> None:
    """Pide credenciales por prompt y valida el login."""
    console.print("\n[bold cyan]── Login de mesero ──[/bold cyan]")
    mesero_id = typer.prompt("  ID del mesero", type=int)
    pin = typer.prompt("  PIN", hide_input=True)
    try:
        mesero = service.login(mesero_id, pin)
        console.print(
            Panel(
                f"[bold green]✅ Bienvenido, [bold cyan]{mesero.nombre}[/bold cyan]![/bold green]\n"
                f"[dim]ID: {mesero.mesero_id}[/dim]",
                title="[bold]Login exitoso[/bold]",
                border_style="green",
            )
        )
    except AppError as e:
        _error(str(e))


def flujo_listar() -> None:
    """Muestra la tabla de todos los meseros."""
    meseros = service.listar_meseros()
    if not meseros:
        console.print(
            Panel("[yellow]No hay meseros registrados aún.[/yellow]", border_style="yellow")
        )
        return
    console.print()
    console.print(_tabla_meseros(meseros))
    console.print(f"\n[dim]Total: {len(meseros)} mesero(s)[/dim]")


def flujo_obtener() -> None:
    """Pide un ID por prompt y muestra el detalle del mesero."""
    console.print("\n[bold cyan]── Buscar mesero ──[/bold cyan]")
    mesero_id = typer.prompt("  ID del mesero", type=int)
    try:
        mesero = service.obtener_mesero(mesero_id)
        console.print()
        console.print(
            Panel(
                f"[bold cyan]ID:[/bold cyan]     {mesero.mesero_id}\n"
                f"[bold cyan]Nombre:[/bold cyan] {mesero.nombre}\n"
                f"[bold cyan]PIN:[/bold cyan]    {'●' * len(mesero.pin)}",
                title="[bold]Detalle del mesero[/bold]",
                border_style="cyan",
            )
        )
    except AppError as e:
        _error(str(e))


def flujo_eliminar() -> None:
    """Pide un ID por prompt y elimina el mesero."""
    console.print("\n[bold cyan]── Eliminar mesero ──[/bold cyan]")
    mesero_id = typer.prompt("  ID del mesero a eliminar", type=int)
    try:
        service.eliminar_mesero(mesero_id)
        _ok(f"Mesero con ID [bold cyan]{mesero_id}[/bold cyan] eliminado correctamente")
    except AppError as e:
        _error(str(e))


# ── Comandos Typer (--flags) ──────────────────────────────────────────────────


@app.command("registrar")
def registrar(
    nombre: str = typer.Option(..., "--nombre", help="Nombre completo"),
    pin: str = typer.Option(..., "--pin", help="PIN de 4 dígitos numéricos"),
) -> None:
    """Registra un nuevo mesero en el sistema."""
    try:
        mesero = Mesero(nombre=nombre, pin=pin)
        service.registrar_mesero(mesero)
        _ok(f"Mesero [bold cyan]{nombre}[/bold cyan] registrado con ID {mesero.mesero_id}")
    except AppError as e:
        _error(str(e))
        raise typer.Exit(code=1)


@app.command("login")
def login(
    mesero_id: int = typer.Option(..., "--id", help="ID del mesero"),
    pin: str = typer.Option(..., "--pin", help="PIN de 4 dígitos"),
) -> None:
    """Valida las credenciales de un mesero."""
    try:
        mesero = service.login(mesero_id, pin)
        console.print(
            Panel(
                f"[bold green]✅ Bienvenido, [bold cyan]{mesero.nombre}[/bold cyan]![/bold green]\n"
                f"[dim]ID: {mesero.mesero_id}[/dim]",
                title="[bold]Login exitoso[/bold]",
                border_style="green",
            )
        )
    except AppError as e:
        _error(str(e))
        raise typer.Exit(code=1)


@app.command("listar")
def listar() -> None:
    """Muestra todos los meseros registrados."""
    flujo_listar()


@app.command("obtener")
def obtener(
    mesero_id: int = typer.Option(..., "--id", help="ID del mesero a buscar"),
) -> None:
    """Muestra los datos de un mesero específico."""
    try:
        mesero = service.obtener_mesero(mesero_id)
        console.print()
        console.print(
            Panel(
                f"[bold cyan]ID:[/bold cyan]     {mesero.mesero_id}\n"
                f"[bold cyan]Nombre:[/bold cyan] {mesero.nombre}\n"
                f"[bold cyan]PIN:[/bold cyan]    {'●' * len(mesero.pin)}",
                title="[bold]Detalle del mesero[/bold]",
                border_style="cyan",
            )
        )
    except AppError as e:
        _error(str(e))
        raise typer.Exit(code=1)


@app.command("eliminar")
def eliminar(
    mesero_id: int = typer.Option(..., "--id", help="ID del mesero a eliminar"),
) -> None:
    """Elimina un mesero por su ID."""
    try:
        service.eliminar_mesero(mesero_id)
        _ok(f"Mesero con ID [bold cyan]{mesero_id}[/bold cyan] eliminado correctamente")
    except AppError as e:
        _error(str(e))
        raise typer.Exit(code=1)

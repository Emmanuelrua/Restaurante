from .exceptions import (
    DatosMeseroInvalidosError,
    MeseroNoEncontradoError,
    MeseroYaExisteError,
    PlatilloNoEncontradoError,
    PlatilloYaExisteError,
)
from .models import Mesero, Platillo
from .storage import MeseroStorage, PlatilloStorage

# ── Servicio de Meseros ───────────────────────────────────────────────────────


class MeseroService:
    """Contiene la lógica de negocio para la gestión de meseros."""

    def __init__(self, storage: MeseroStorage) -> None:
        """Inicializa el servicio con su capa de almacenamiento."""
        self.storage = storage

    # ── Operaciones públicas ──────────────────────────────────────────────────

    def registrar_mesero(self, mesero: Mesero) -> None:
        """Registra un nuevo mesero si no existe uno con el mismo id."""
        meseros = self.storage.cargar()
        self._verificar_que_no_existe(mesero.mesero_id, meseros)
        self._persistir_mesero(mesero, meseros)

    def login(self, mesero_id: int, pin: str) -> Mesero:
        """Valida las credenciales del mesero y lo retorna si son correctas."""
        meseros = self.storage.cargar()
        mesero = self._buscar_por_id(mesero_id, meseros)
        self._verificar_pin(pin, mesero)
        return mesero

    def obtener_mesero(self, mesero_id: int) -> Mesero:
        """Retorna el mesero con el id dado o lanza error si no existe."""
        meseros = self.storage.cargar()
        return self._buscar_por_id(mesero_id, meseros)

    def listar_meseros(self) -> list[Mesero]:
        """Retorna la lista completa de meseros registrados."""
        return self.storage.cargar()

    def eliminar_mesero(self, mesero_id: int) -> None:
        """Elimina el mesero con el id dado o lanza error si no existe."""
        meseros = self.storage.cargar()
        filtrados = [m for m in meseros if m.mesero_id != mesero_id]

        if len(filtrados) == len(meseros):
            raise MeseroNoEncontradoError(mesero_id)

        self.storage.guardar(filtrados)

    # ── Helpers privados ──────────────────────────────────────────────────────

    def _buscar_por_id(self, mesero_id: int, meseros: list[Mesero]) -> Mesero:
        """Busca un mesero por id dentro de una lista ya cargada."""
        for mesero in meseros:
            if mesero.mesero_id == mesero_id:
                return mesero
        raise MeseroNoEncontradoError(mesero_id)

    def _verificar_que_no_existe(self, mesero_id: int, meseros: list[Mesero]) -> None:
        """Lanza error si ya existe un mesero con el id dado."""
        if any(m.mesero_id == mesero_id for m in meseros):
            raise MeseroYaExisteError(mesero_id)

    def _verificar_pin(self, pin: str, mesero: Mesero) -> None:
        """Lanza error si el pin no coincide con el del mesero."""
        if mesero.pin != pin:
            raise DatosMeseroInvalidosError("Pin incorrecto")

    def _persistir_mesero(self, mesero: Mesero, meseros: list[Mesero]) -> None:
        """Agrega el mesero a la lista y la guarda en storage."""
        meseros.append(mesero)
        self.storage.guardar(meseros)


# ── Servicio de Platillos ─────────────────────────────────────────────────────


class PlatilloService:
    """Contiene la lógica de negocio para el CRUD del menú de platillos."""

    def __init__(self, storage: PlatilloStorage) -> None:
        """Inicializa el servicio con su capa de almacenamiento."""
        self.storage = storage

    # ── Operaciones públicas ──────────────────────────────────────────────────

    def crear_platillo(self, platillo: Platillo) -> None:
        """Agrega un platillo al menú si no existe uno con el mismo id."""
        platillos = self.storage.cargar()
        self._verificar_que_no_existe(platillo.platillo_id, platillos)
        self._persistir_platillo(platillo, platillos)

    def obtener_platillo(self, platillo_id: int) -> Platillo:
        """Retorna el platillo con el id dado o lanza error si no existe."""
        platillos = self.storage.cargar()
        return self._buscar_por_id(platillo_id, platillos)

    def listar_platillos(self) -> list[Platillo]:
        """Retorna todos los platillos del menú."""
        return self.storage.cargar()

    def listar_por_categoria(self, categoria: str) -> list[Platillo]:
        """Retorna los platillos filtrados por categoría."""
        platillos = self.storage.cargar()
        return [p for p in platillos if p.categoria == categoria]

    def actualizar_platillo(
        self, platillo_id: int, nombre: str, precio: float, categoria: str
    ) -> None:
        """Actualiza los datos de un platillo existente."""
        platillos = self.storage.cargar()
        platillo = self._buscar_por_id(platillo_id, platillos)
        self._aplicar_cambios(platillo, nombre, precio, categoria)
        self.storage.guardar(platillos)

    def eliminar_platillo(self, platillo_id: int) -> None:
        """Elimina el platillo con el id dado o lanza error si no existe."""
        platillos = self.storage.cargar()
        filtrados = [p for p in platillos if p.platillo_id != platillo_id]

        if len(filtrados) == len(platillos):
            raise PlatilloNoEncontradoError(platillo_id)

        self.storage.guardar(filtrados)

    # ── Helpers privados ──────────────────────────────────────────────────────

    def _buscar_por_id(self, platillo_id: int, platillos: list[Platillo]) -> Platillo:
        """Busca un platillo por id dentro de una lista ya cargada."""
        for platillo in platillos:
            if platillo.platillo_id == platillo_id:
                return platillo
        raise PlatilloNoEncontradoError(platillo_id)

    def _verificar_que_no_existe(self, platillo_id: int, platillos: list[Platillo]) -> None:
        """Lanza error si ya existe un platillo con el id dado."""
        if any(p.platillo_id == platillo_id for p in platillos):
            raise PlatilloYaExisteError(platillo_id)

    def _aplicar_cambios(
        self, platillo: Platillo, nombre: str, precio: float, categoria: str
    ) -> None:
        """Aplica los nuevos valores al platillo (sin crear uno nuevo)."""
        platillo.nombre = nombre.strip()
        platillo.precio = precio
        platillo.categoria = categoria

    def _persistir_platillo(self, platillo: Platillo, platillos: list[Platillo]) -> None:
        """Agrega el platillo a la lista y la guarda en storage."""
        platillos.append(platillo)
        self.storage.guardar(platillos)

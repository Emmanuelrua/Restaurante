from dataclasses import dataclass

from .exceptions import (
    CategoriaInvalidaError,
    DatosMeseroInvalidosError,
    DatosPlatilloInvalidosError,
)

CATEGORIAS_VALIDAS = {"entrada", "plato_fuerte", "postre", "bebida"}


@dataclass
class Mesero:
    """Representa un mesero registrado en el sistema del restaurante."""

    mesero_id: int
    nombre: str
    pin: str

    def __post_init__(self) -> None:
        """Valida los datos del mesero al momento de crearlo."""
        self._validar_id(self.mesero_id)
        self._validar_nombre(self.nombre)
        self._validar_pin(self.pin)

    def _validar_id(self, mesero_id: int) -> None:
        """Verifica que el id sea un entero positivo."""
        if mesero_id <= 0:
            raise DatosMeseroInvalidosError("El id del mesero debe ser un entero positivo")

    def _validar_nombre(self, nombre: str) -> None:
        """Verifica que el nombre no esté vacío."""
        if not nombre.strip():
            raise DatosMeseroInvalidosError("El nombre del mesero no puede estar vacío")

    def _validar_pin(self, pin: str) -> None:
        """Verifica que el pin tenga exactamente 4 dígitos numéricos."""
        if not pin.isdigit() or len(pin) != 4:
            raise DatosMeseroInvalidosError("El pin debe tener exactamente 4 dígitos numéricos")


@dataclass
class Platillo:
    """Representa un platillo del menú del restaurante."""

    platillo_id: int
    nombre: str
    precio: float
    categoria: str
    disponible: bool = True

    def __post_init__(self) -> None:
        """Valida los datos del platillo al momento de crearlo."""
        self._validar_id(self.platillo_id)
        self._validar_nombre(self.nombre)
        self._validar_precio(self.precio)
        self._validar_categoria(self.categoria)

    def _validar_id(self, platillo_id: int) -> None:
        """Verifica que el id sea un entero positivo."""
        if platillo_id <= 0:
            raise DatosPlatilloInvalidosError("El id del platillo debe ser un entero positivo")

    def _validar_nombre(self, nombre: str) -> None:
        """Verifica que el nombre no esté vacío."""
        if not nombre.strip():
            raise DatosPlatilloInvalidosError("El nombre del platillo no puede estar vacío")

    def _validar_precio(self, precio: float) -> None:
        """Verifica que el precio sea mayor a cero."""
        if precio <= 0:
            raise DatosPlatilloInvalidosError("El precio debe ser mayor a cero")

    def _validar_categoria(self, categoria: str) -> None:
        """Verifica que la categoría sea una de las permitidas."""
        if categoria not in CATEGORIAS_VALIDAS:
            raise CategoriaInvalidaError(categoria)

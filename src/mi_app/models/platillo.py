"""Modelo de datos para la entidad Platillo."""

from dataclasses import dataclass

from ..exceptions import CategoriaInvalidaError, DatosPlatilloInvalidosError

CATEGORIAS_VALIDAS = {"entrada", "plato_fuerte", "postre", "bebida"}


@dataclass
class Platillo:
    """Representa un platillo del menú del restaurante.

    Attributes:
        nombre: Nombre del platillo.
        precio: Precio en pesos colombianos.
        categoria: Tipo de platillo (entrada, plato_fuerte, postre, bebida).
        disponible: Indica si el platillo está disponible en el menú.
        platillo_id: Identificador único asignado automáticamente por el almacenamiento.
    """

    nombre: str
    precio: float
    categoria: str
    disponible: bool = True
    platillo_id: int | None = None

    def __post_init__(self) -> None:
        """Valida los datos del platillo al momento de crearlo."""
        self._validar_id()
        self._validar_nombre()
        self._validar_precio()
        self._validar_categoria()

    def _validar_id(self) -> None:
        """Verifica que el id, si ya fue asignado, sea un entero positivo."""
        if self.platillo_id is not None and self.platillo_id <= 0:
            raise DatosPlatilloInvalidosError("El id del platillo debe ser un entero positivo")

    def _validar_nombre(self) -> None:
        """Verifica que el nombre no esté vacío."""
        if not self.nombre.strip():
            raise DatosPlatilloInvalidosError("El nombre del platillo no puede estar vacío")

    def _validar_precio(self) -> None:
        """Verifica que el precio sea mayor a cero."""
        if self.precio <= 0:
            raise DatosPlatilloInvalidosError("El precio debe ser mayor a cero")

    def _validar_categoria(self) -> None:
        """Verifica que la categoría sea una de las permitidas."""
        if self.categoria not in CATEGORIAS_VALIDAS:
            raise CategoriaInvalidaError(self.categoria)

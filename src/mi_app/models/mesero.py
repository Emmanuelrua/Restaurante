"""Modelo de datos para la entidad Mesero."""

from dataclasses import dataclass

from ..exceptions import DatosMeseroInvalidosError


@dataclass
class Mesero:
    """Representa un mesero registrado en el sistema del restaurante.

    Attributes:
        nombre: Nombre completo del mesero.
        pin: Clave numérica de 4 dígitos para autenticación.
        mesero_id: Identificador único asignado automáticamente por el almacenamiento.
    """

    nombre: str
    pin: str
    mesero_id: int | None = None

    def __post_init__(self) -> None:
        """Valida los datos del mesero al momento de crearlo."""
        self._validar_id()
        self._validar_nombre()
        self._validar_pin()

    def _validar_id(self) -> None:
        """Verifica que el id, si ya fue asignado, sea un entero positivo."""
        if self.mesero_id is not None and self.mesero_id <= 0:
            raise DatosMeseroInvalidosError("El id del mesero debe ser un entero positivo")

    def _validar_nombre(self) -> None:
        """Verifica que el nombre no esté vacío."""
        if not self.nombre.strip():
            raise DatosMeseroInvalidosError("El nombre del mesero no puede estar vacío")

    def _validar_pin(self) -> None:
        """Verifica que el pin tenga exactamente 4 dígitos numéricos."""
        if not self.pin.isdigit() or len(self.pin) != 4:
            raise DatosMeseroInvalidosError("El pin debe tener exactamente 4 dígitos numéricos")

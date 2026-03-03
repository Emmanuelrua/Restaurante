class AppError(Exception):
    """Base class for all application-specific exceptions."""

    pass


# ── Mesero ────────────────────────────────────────────────────────────────────


class MeseroError(AppError):
    """Clase base para mesero-related exceptions."""

    pass


class MeseroNoEncontradoError(MeseroError):
    """Se lanza cuando no se encuentra un mesero con el id dado."""

    def __init__(self, mesero_id: int) -> None:
        self.mesero_id = mesero_id
        super().__init__(f"Mesero con id {mesero_id} no encontrado")


class MeseroYaExisteError(MeseroError):
    """Se lanza cuando se intenta registrar un mesero con un id ya existente."""

    def __init__(self, mesero_id: int) -> None:
        self.mesero_id = mesero_id
        super().__init__(f"Mesero con id {mesero_id} ya existe")


class DatosMeseroInvalidosError(MeseroError):
    """Se lanza cuando los datos de un mesero no pasan la validación."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)


# ── Platillo ──────────────────────────────────────────────────────────────────


class PlatilloError(AppError):
    """Clase Base para platillo-related exceptions."""

    pass


class PlatilloNoEncontradoError(PlatilloError):
    """Se lanza cuando no se encuentra un platillo con el id dado."""

    def __init__(self, platillo_id: int) -> None:
        self.platillo_id = platillo_id
        super().__init__(f"Platillo con id {platillo_id} no encontrado")


class PlatilloYaExisteError(PlatilloError):
    """Se lanza cuando se intenta crear un platillo con un id ya existente."""

    def __init__(self, platillo_id: int) -> None:
        self.platillo_id = platillo_id
        super().__init__(f"Platillo con id {platillo_id} ya existe")


class DatosPlatilloInvalidosError(PlatilloError):
    """Se lanza cuando los datos de un platillo no pasan la validación."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)


class CategoriaInvalidaError(PlatilloError):
    """Se lanza cuando se usa una categoría que no está permitida."""

    CATEGORIAS_VALIDAS = {"entrada", "plato_fuerte", "postre", "bebida"}

    def __init__(self, categoria: str) -> None:
        self.categoria = categoria
        super().__init__(f"Categoría '{categoria}' no válida. Opciones: {self.CATEGORIAS_VALIDAS}")

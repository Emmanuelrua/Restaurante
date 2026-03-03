# tests/test_services.py
from unittest.mock import MagicMock

import pytest

from src.mi_app.exceptions import (
    CategoriaInvalidaError,
    DatosMeseroInvalidosError,
    DatosPlatilloInvalidosError,
    MeseroNoEncontradoError,
    MeseroYaExisteError,
    PlatilloNoEncontradoError,
    PlatilloYaExisteError,
)
from src.mi_app.models import Mesero, Platillo
from src.mi_app.services import MeseroService, PlatilloService

# ── Tests de Meseros ──────────────────────────────────────────────────────────


def test_registrar_mesero_exitoso():
    """Verifica que un mesero nuevo se registra correctamente."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = []

    service = MeseroService(mock_storage)
    mesero = Mesero(mesero_id=1, nombre="Carlos", pin="1234")

    service.registrar_mesero(mesero)

    mock_storage.guardar.assert_called_once()


def test_registrar_mesero_id_duplicado():
    """Verifica que se lanza error al registrar un mesero con id existente."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = [Mesero(mesero_id=1, nombre="Carlos", pin="1234")]

    service = MeseroService(mock_storage)
    mesero_nuevo = Mesero(mesero_id=1, nombre="Luis", pin="5678")

    with pytest.raises(MeseroYaExisteError):
        service.registrar_mesero(mesero_nuevo)

    mock_storage.guardar.assert_not_called()


def test_login_exitoso():
    """Verifica que el login retorna el mesero cuando el pin es correcto."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = [Mesero(mesero_id=1, nombre="Carlos", pin="1234")]

    service = MeseroService(mock_storage)
    mesero = service.login(1, "1234")

    assert mesero.nombre == "Carlos"


def test_login_pin_incorrecto():
    """Verifica que el login lanza error cuando el pin no coincide."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = [Mesero(mesero_id=1, nombre="Carlos", pin="1234")]

    service = MeseroService(mock_storage)

    with pytest.raises(DatosMeseroInvalidosError):
        service.login(1, "0000")


def test_login_mesero_no_encontrado():
    """Verifica que el login lanza error cuando el mesero no existe."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = []

    service = MeseroService(mock_storage)

    with pytest.raises(MeseroNoEncontradoError):
        service.login(99, "1234")


def test_eliminar_mesero_exitoso():
    """Verifica que un mesero existente se elimina correctamente."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = [Mesero(mesero_id=1, nombre="Carlos", pin="1234")]

    service = MeseroService(mock_storage)
    service.eliminar_mesero(1)

    mock_storage.guardar.assert_called_once_with([])


def test_mesero_pin_invalido():
    """Verifica que se lanza error al crear un mesero con pin no numérico."""
    with pytest.raises(DatosMeseroInvalidosError):
        Mesero(mesero_id=1, nombre="Carlos", pin="abcd")


# ── Tests de Platillos ────────────────────────────────────────────────────────


def test_crear_platillo_exitoso():
    """Verifica que un platillo nuevo se crea correctamente en el menú."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = []

    service = PlatilloService(mock_storage)
    platillo = Platillo(platillo_id=1, nombre="Sopa del día", precio=12000.0, categoria="entrada")

    service.crear_platillo(platillo)

    mock_storage.guardar.assert_called_once()


def test_crear_platillo_id_duplicado():
    """Verifica que se lanza error al crear un platillo con id existente."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = [
        Platillo(platillo_id=1, nombre="Sopa del día", precio=12000.0, categoria="entrada")
    ]

    service = PlatilloService(mock_storage)
    platillo_nuevo = Platillo(platillo_id=1, nombre="Ensalada", precio=8000.0, categoria="entrada")

    with pytest.raises(PlatilloYaExisteError):
        service.crear_platillo(platillo_nuevo)

    mock_storage.guardar.assert_not_called()


def test_obtener_platillo_no_encontrado():
    """Verifica que se lanza error al buscar un platillo inexistente."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = []

    service = PlatilloService(mock_storage)

    with pytest.raises(PlatilloNoEncontradoError):
        service.obtener_platillo(99)


def test_listar_por_categoria():
    """Verifica que el filtro por categoría retorna solo los platillos correctos."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = [
        Platillo(platillo_id=1, nombre="Sopa", precio=12000.0, categoria="entrada"),
        Platillo(platillo_id=2, nombre="Bandeja paisa", precio=32000.0, categoria="plato_fuerte"),
    ]

    service = PlatilloService(mock_storage)
    entradas = service.listar_por_categoria("entrada")

    assert len(entradas) == 1
    assert entradas[0].nombre == "Sopa"


def test_eliminar_platillo_exitoso():
    """Verifica que un platillo existente se elimina correctamente."""
    mock_storage = MagicMock()
    mock_storage.cargar.return_value = [
        Platillo(platillo_id=1, nombre="Sopa", precio=12000.0, categoria="entrada")
    ]

    service = PlatilloService(mock_storage)
    service.eliminar_platillo(1)

    mock_storage.guardar.assert_called_once_with([])


def test_platillo_categoria_invalida():
    """Verifica que se lanza error al crear un platillo con categoría no permitida."""
    with pytest.raises(CategoriaInvalidaError):
        Platillo(platillo_id=1, nombre="Algo raro", precio=5000.0, categoria="snack")


def test_platillo_precio_invalido():
    """Verifica que se lanza error al crear un platillo con precio negativo."""
    with pytest.raises(DatosPlatilloInvalidosError):
        Platillo(platillo_id=1, nombre="Sopa", precio=-100.0, categoria="entrada")

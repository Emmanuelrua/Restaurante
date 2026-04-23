# tests/test_supabase.py
"""Tests de integración con Supabase.

Estos tests requieren que SUPABASE_URL y SUPABASE_KEY estén definidos en el
entorno (archivo .env en la raíz del proyecto).  Si las variables no están
presentes el test se omite automáticamente con ``pytest.skip``, de modo que
no bloquean el pipeline de CI cuando no se dispone de credenciales.
"""

import os

import pytest

from src.mi_app.models import Mesero, Platillo
from src.mi_app.storage_supabase import MeseroSupabaseStorage, PlatilloSupabaseStorage

# ── Fixture de salto automático ───────────────────────────────────────────────

REQUIERE_SUPABASE = pytest.mark.skipif(
    not (os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_KEY")),
    reason="SUPABASE_URL o SUPABASE_KEY no están definidos en el entorno",
)

# ── Tests de conexión y lectura ───────────────────────────────────────────────


@REQUIERE_SUPABASE
def test_conexion_meseros():
    """Verifica que la tabla meseros es accesible en Supabase."""
    storage = MeseroSupabaseStorage()
    meseros = storage.cargar()
    assert isinstance(meseros, list)


@REQUIERE_SUPABASE
def test_conexion_platillos():
    """Verifica que la tabla platillos es accesible en Supabase."""
    storage = PlatilloSupabaseStorage()
    platillos = storage.cargar()
    assert isinstance(platillos, list)


@REQUIERE_SUPABASE
def test_meseros_tienen_campos_requeridos():
    """Verifica que los meseros cargados tienen todos sus campos."""
    storage = MeseroSupabaseStorage()
    meseros = storage.cargar()
    for m in meseros:
        assert isinstance(m, Mesero)
        assert m.mesero_id is not None and m.mesero_id > 0
        assert m.nombre.strip()
        assert len(m.pin) == 4 and m.pin.isdigit()


@REQUIERE_SUPABASE
def test_platillos_tienen_campos_requeridos():
    """Verifica que los platillos cargados tienen todos sus campos."""
    storage = PlatilloSupabaseStorage()
    platillos = storage.cargar()
    for p in platillos:
        assert isinstance(p, Platillo)
        assert p.platillo_id is not None and p.platillo_id > 0
        assert p.nombre.strip()
        assert p.precio > 0
        assert p.categoria in {"entrada", "plato_fuerte", "postre", "bebida"}

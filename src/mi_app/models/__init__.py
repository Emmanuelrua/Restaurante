"""Paquete de modelos del sistema de restaurante."""

from .mesero import Mesero
from .platillo import CATEGORIAS_VALIDAS, Platillo

__all__ = ["Mesero", "Platillo", "CATEGORIAS_VALIDAS"]
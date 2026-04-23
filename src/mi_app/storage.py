import json
from dataclasses import asdict
from pathlib import Path
from typing import Protocol

from .models import Mesero, Platillo

# ── Protocols ─────────────────────────────────────────────────────────────────


class MeseroStorage(Protocol):
    """Define el contrato que debe cumplir cualquier almacenamiento de meseros."""

    def cargar(self) -> list[Mesero]: ...

    def guardar(self, meseros: list[Mesero]) -> None: ...


class PlatilloStorage(Protocol):
    """Define el contrato que debe cumplir cualquier almacenamiento de platillos."""

    def cargar(self) -> list[Platillo]: ...

    def guardar(self, platillos: list[Platillo]) -> None: ...


# ── Implementaciones JSON ─────────────────────────────────────────────────────


class MeseroJSONStorage:
    """Lee y escribe meseros desde/hacia un archivo JSON."""

    def __init__(self, filepath: Path) -> None:
        """Inicializa el storage con la ruta del archivo JSON."""
        self.filepath = filepath

    def cargar(self) -> list[Mesero]:
        """Carga la lista de meseros desde el archivo JSON."""
        if not self.filepath.exists():
            return []

        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [Mesero(**item) for item in data]

    def guardar(self, meseros: list[Mesero]) -> None:
        """Persiste la lista de meseros en el archivo JSON.

        Asigna automáticamente un ``mesero_id`` a los registros nuevos
        cuyo id todavía sea ``None``, tomando como base el mayor id existente.
        """
        ids_asignados = {m.mesero_id for m in meseros if m.mesero_id is not None}
        siguiente_id = max(ids_asignados, default=0) + 1
        for m in meseros:
            if m.mesero_id is None:
                m.mesero_id = siguiente_id
                siguiente_id += 1

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([asdict(m) for m in meseros], f, indent=2, ensure_ascii=False)


class PlatilloJSONStorage:
    """Lee y escribe platillos desde/hacia un archivo JSON."""

    def __init__(self, filepath: Path) -> None:
        """Inicializa el storage con la ruta del archivo JSON."""
        self.filepath = filepath

    def cargar(self) -> list[Platillo]:
        """Carga la lista de platillos desde el archivo JSON."""
        if not self.filepath.exists():
            return []

        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [Platillo(**item) for item in data]

    def guardar(self, platillos: list[Platillo]) -> None:
        """Persiste la lista de platillos en el archivo JSON.

        Asigna automáticamente un ``platillo_id`` a los registros nuevos
        cuyo id todavía sea ``None``, tomando como base el mayor id existente.
        """
        ids_asignados = {p.platillo_id for p in platillos if p.platillo_id is not None}
        siguiente_id = max(ids_asignados, default=0) + 1
        for p in platillos:
            if p.platillo_id is None:
                p.platillo_id = siguiente_id
                siguiente_id += 1

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([asdict(p) for p in platillos], f, indent=2, ensure_ascii=False)

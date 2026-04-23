"""Implementaciones de Storage que persisten datos usando la API REST de Supabase.

Cada clase implementa el mismo contrato (Protocol) que las implementaciones JSON,
por lo que los servicios no necesitan saber con qué backend están hablando.

Configuración requerida (variables de entorno, cargadas desde .env):
    SUPABASE_URL  — URL del proyecto Supabase (ej. https://abc123.supabase.co)
    SUPABASE_KEY  — anon key o service_role key del proyecto
"""

import os

import requests

from .models import Mesero, Platillo

# ── Helpers internos ──────────────────────────────────────────────────────────


def _base() -> str:
    """Retorna la URL base de la API REST del proyecto Supabase configurado."""
    url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    if not url:
        raise RuntimeError("SUPABASE_URL no está definido. Revisa tu archivo .env.")
    return f"{url}/rest/v1"


def _headers(prefer: str = "return=representation") -> dict[str, str]:
    """Construye las cabeceras HTTP necesarias para autenticarse en Supabase.

    Args:
        prefer: Valor del header ``Prefer`` que controla la respuesta de PostgREST
                (ej. ``return=representation`` para recibir los registros afectados,
                ``return=minimal`` para no recibir cuerpo de respuesta).
    """
    key = os.environ.get("SUPABASE_KEY", "")
    if not key:
        raise RuntimeError("SUPABASE_KEY no está definido. Revisa tu archivo .env.")
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": prefer,
    }


def _check(resp: requests.Response) -> None:
    """Valida que la respuesta HTTP sea exitosa (2xx).

    Lanza ``RuntimeError`` con el mensaje de error de Supabase si el código
    de estado indica un fallo, para que la capa de servicio reciba una
    excepción descriptiva.
    """
    try:
        resp.raise_for_status()
    except requests.HTTPError as exc:
        detalle = resp.text or str(exc)
        raise RuntimeError(f"Error en Supabase ({resp.status_code}): {detalle}") from exc


# ── Almacenamiento de meseros ─────────────────────────────────────────────────


class MeseroSupabaseStorage:
    """Lee y escribe meseros usando la API REST de Supabase (PostgREST).

    Implementa el mismo contrato que ``MeseroJSONStorage``; los servicios
    no distinguen entre una u otra implementación.

    Operaciones:
        - ``cargar``  → GET  /rest/v1/meseros
        - ``guardar`` → POST /rest/v1/meseros (INSERT o UPSERT) + DELETE de huérfanos
    """

    def cargar(self) -> list[Mesero]:
        """Carga la lista de meseros desde la tabla ``meseros`` en Supabase."""
        resp = requests.get(
            f"{_base()}/meseros",
            headers=_headers(),
            params={"order": "mesero_id.asc"},
        )
        _check(resp)
        return [Mesero(**row) for row in resp.json()]

    def guardar(self, meseros: list[Mesero]) -> None:
        """Sincroniza la lista de meseros con la tabla ``meseros`` en Supabase.

        Los meseros sin ``mesero_id`` se insertan como registros nuevos; la columna
        SERIAL de PostgreSQL genera el ID y se asigna de vuelta al objeto en memoria.
        Los meseros con ID existente se actualizan mediante UPSERT.
        Al final se eliminan los registros que ya no forman parte de la lista.
        """
        base = _base()

        # Separar antes de que los nuevos reciban su ID
        nuevos = [m for m in meseros if m.mesero_id is None]
        existentes = [m for m in meseros if m.mesero_id is not None]

        # INSERT de nuevos registros; PostgreSQL asigna el SERIAL
        if nuevos:
            resp = requests.post(
                f"{base}/meseros",
                headers=_headers("return=representation"),
                json=[{"nombre": m.nombre, "pin": m.pin} for m in nuevos],
            )
            _check(resp)
            for m, row in zip(nuevos, resp.json()):
                m.mesero_id = row["mesero_id"]

        # UPSERT de registros que ya tienen ID (actualiza campos si cambiaron)
        if existentes:
            upsert_resp = requests.post(
                f"{base}/meseros",
                headers=_headers("resolution=merge-duplicates,return=minimal"),
                json=[
                    {"mesero_id": m.mesero_id, "nombre": m.nombre, "pin": m.pin}
                    for m in existentes
                ],
            )
            _check(upsert_resp)

        # Eliminar registros que ya no están en la lista
        ids_actuales = [m.mesero_id for m in meseros]
        if ids_actuales:
            ids_str = ",".join(str(mid) for mid in ids_actuales)
            del_resp = requests.delete(
                f"{base}/meseros?mesero_id=not.in.({ids_str})",
                headers=_headers("return=minimal"),
            )
            _check(del_resp)
        else:
            # Lista vacía: borrar todos; se filtra por gte.0 porque la API
            # requiere al menos un filtro para operaciones de borrado masivo
            del_resp = requests.delete(
                f"{base}/meseros?mesero_id=gte.0",
                headers=_headers("return=minimal"),
            )
            _check(del_resp)


# ── Almacenamiento de platillos ───────────────────────────────────────────────


class PlatilloSupabaseStorage:
    """Lee y escribe platillos usando la API REST de Supabase (PostgREST).

    Implementa el mismo contrato que ``PlatilloJSONStorage``; los servicios
    no distinguen entre una u otra implementación.

    Operaciones:
        - ``cargar``  → GET  /rest/v1/platillos
        - ``guardar`` → POST /rest/v1/platillos (INSERT o UPSERT) + DELETE de huérfanos
    """

    def cargar(self) -> list[Platillo]:
        """Carga la lista de platillos desde la tabla ``platillos`` en Supabase."""
        resp = requests.get(
            f"{_base()}/platillos",
            headers=_headers(),
            params={"order": "platillo_id.asc"},
        )
        _check(resp)
        return [
            Platillo(
                platillo_id=row["platillo_id"],
                nombre=row["nombre"],
                # precio viene como Decimal de PostgreSQL; se convierte a float
                precio=float(row["precio"]),
                categoria=row["categoria"],
                disponible=row["disponible"],
            )
            for row in resp.json()
        ]

    def guardar(self, platillos: list[Platillo]) -> None:
        """Sincroniza la lista de platillos con la tabla ``platillos`` en Supabase.

        Los platillos sin ``platillo_id`` se insertan como registros nuevos; la columna
        SERIAL de PostgreSQL genera el ID y se asigna de vuelta al objeto en memoria.
        Los platillos con ID existente se actualizan mediante UPSERT.
        Al final se eliminan los registros que ya no forman parte de la lista.
        """
        base = _base()

        nuevos = [p for p in platillos if p.platillo_id is None]
        existentes = [p for p in platillos if p.platillo_id is not None]

        # INSERT de nuevos registros; PostgreSQL asigna el SERIAL
        if nuevos:
            resp = requests.post(
                f"{base}/platillos",
                headers=_headers("return=representation"),
                json=[
                    {
                        "nombre": p.nombre,
                        "precio": p.precio,
                        "categoria": p.categoria,
                        "disponible": p.disponible,
                    }
                    for p in nuevos
                ],
            )
            _check(resp)
            for p, row in zip(nuevos, resp.json()):
                p.platillo_id = row["platillo_id"]

        # UPSERT de registros que ya tienen ID
        if existentes:
            upsert_resp = requests.post(
                f"{base}/platillos",
                headers=_headers("resolution=merge-duplicates,return=minimal"),
                json=[
                    {
                        "platillo_id": p.platillo_id,
                        "nombre": p.nombre,
                        "precio": p.precio,
                        "categoria": p.categoria,
                        "disponible": p.disponible,
                    }
                    for p in existentes
                ],
            )
            _check(upsert_resp)

        # Eliminar registros que ya no están en la lista
        ids_actuales = [p.platillo_id for p in platillos]
        if ids_actuales:
            ids_str = ",".join(str(pid) for pid in ids_actuales)
            del_resp = requests.delete(
                f"{base}/platillos?platillo_id=not.in.({ids_str})",
                headers=_headers("return=minimal"),
            )
            _check(del_resp)
        else:
            del_resp = requests.delete(
                f"{base}/platillos?platillo_id=gte.0",
                headers=_headers("return=minimal"),
            )
            _check(del_resp)

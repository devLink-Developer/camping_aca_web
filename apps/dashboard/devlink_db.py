from __future__ import annotations

import os
from typing import Any, Iterable

import psycopg2


def _get_env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or str(raw).strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def get_devlink_config() -> dict[str, Any]:
    """Connection settings for the Devlink DB.

    Uses env vars when present:
    - DEVLINK_DB_HOST
    - DEVLINK_DB_PORT_INTERNAL
    - DEVLINK_DB_PORT_EXTERNAL
    - DEVLINK_DB_NAME
    - DEVLINK_DB_USER
    - DEVLINK_DB_PASSWORD

    Defaults match the production details provided in the task.
    """

    # IMPORTANT: This connection targets the Devlink production DB, not the app's primary DB.
    # Do NOT fall back to DB_HOST/DB_NAME/DB_USER, because those refer to this project's DB.
    host = os.getenv("DEVLINK_DB_HOST", "200.58.107.187")
    dbname = os.getenv("DEVLINK_DB_NAME", "devlink")
    user = os.getenv("DEVLINK_DB_USER", "devlink")
    password = os.getenv("DEVLINK_DB_PASSWORD", "@Inf124578..")

    return {
        "host": host,
        "port_internal": _get_env_int("DEVLINK_DB_PORT_INTERNAL", 5455),
        "port_external": _get_env_int("DEVLINK_DB_PORT_EXTERNAL", 5456),
        "dbname": dbname,
        "user": user,
        "password": password,
        "sslmode": os.getenv("DEVLINK_DB_SSLMODE", "prefer"),
        "connect_timeout": _get_env_int("DEVLINK_DB_CONNECT_TIMEOUT", 6),
    }


def connect_devlink(*, readonly: bool = True):
    """Connects to Devlink DB, trying internal port first then external fallback.

    Returns (connection, used_port).
    """

    cfg = get_devlink_config()
    last_exc: Exception | None = None

    for port in (cfg["port_internal"], cfg["port_external"]):
        try:
            conn = psycopg2.connect(
                host=cfg["host"],
                port=port,
                user=cfg["user"],
                password=cfg["password"],
                dbname=cfg["dbname"],
                connect_timeout=cfg["connect_timeout"],
                sslmode=cfg["sslmode"],
            )
            conn.set_session(readonly=readonly, autocommit=True)
            return conn, port
        except Exception as exc:  # noqa: BLE001
            last_exc = exc

    raise RuntimeError(
        f"No se pudo conectar a Devlink DB en {cfg['host']}:{cfg['port_internal']} (interno) ni {cfg['port_external']} (externo)."
    ) from last_exc


def fetch_one(conn, sql: str, params: Iterable[Any] | None = None):
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        row = cur.fetchone()
    return row


def fetch_all(conn, sql: str, params: Iterable[Any] | None = None):
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        rows = cur.fetchall()
    return rows


def execute(conn, sql: str, params: Iterable[Any] | None = None) -> None:
    with conn.cursor() as cur:
        cur.execute(sql, params or ())

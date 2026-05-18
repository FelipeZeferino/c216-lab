import os
from pathlib import Path

import asyncpg


INIT_SQL_PATH = Path(__file__).with_name("init.sql")


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is required")
    return database_url


async def get_connection() -> asyncpg.Connection:
    return await asyncpg.connect(get_database_url())


async def init_db() -> None:
    conn = await get_connection()
    try:
        await conn.execute(INIT_SQL_PATH.read_text(encoding="utf-8"))
    finally:
        await conn.close()

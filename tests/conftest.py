import asyncio

import asyncpg
import pytest
from fastapi.testclient import TestClient

from app.db.connection import get_database_url, init_db
from app.main import app


async def _reset_database() -> None:
    conn = await asyncpg.connect(get_database_url())
    try:
        await conn.execute("DELETE FROM alunos")
        await conn.execute("ALTER SEQUENCE alunos_ges_matricula_seq RESTART WITH 1")
        await conn.execute("ALTER SEQUENCE alunos_gec_matricula_seq RESTART WITH 1")
    finally:
        await conn.close()


@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    asyncio.run(init_db())


@pytest.fixture(autouse=True)
def reset_database():
    asyncio.run(_reset_database())
    yield
    asyncio.run(_reset_database())


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

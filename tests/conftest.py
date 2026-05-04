import pytest

from app.services.aluno_service import aluno_service


@pytest.fixture(autouse=True)
def reset_aluno_service():
    aluno_service.reset_state(reset_counters=True)
    yield
    aluno_service.reset_state(reset_counters=True)


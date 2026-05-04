# Prática 4 - CRUD de Alunos com FastAPI

## Como executar localmente

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Como executar com Docker Compose

```bash
docker compose up --build
```

## Como rodar os testes

```bash
pytest
docker compose run tests
```

## Endpoints principais

- `POST /api/v1/alunos/`
- `GET /api/v1/alunos/`
- `GET /api/v1/alunos/{aluno_id}`
- `PATCH /api/v1/alunos/{aluno_id}`
- `DELETE /api/v1/alunos/{aluno_id}`
- `DELETE /api/v1/alunos/`

## Observações

- Os cursos suportados são `GES` e `GEC`.
- O ID do aluno segue o formato `CURSO + matricula`, por exemplo `GES1`.
- A limpeza total da lista nao reutiliza IDs ja emitidos.

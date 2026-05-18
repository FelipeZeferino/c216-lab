from fastapi import FastAPI

from app.db.connection import init_db
from app.middlewares.custom_header import add_custom_header
from app.middlewares.logging import log_requests
from app.routes.aluno_routes import router as aluno_router


app = FastAPI(
    title="Gerenciador de Alunos API",
    description="API para estudo de CRUD, middlewares, testes e Docker com FastAPI",
    version="1.0.0",
)

app.middleware("http")(log_requests)
app.middleware("http")(add_custom_header)

app.include_router(aluno_router)


@app.on_event("startup")
async def startup() -> None:
    await init_db()


@app.get("/")
def root():
    return {"mensagem": "API funcionando"}

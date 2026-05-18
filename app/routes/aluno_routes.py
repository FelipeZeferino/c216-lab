from fastapi import APIRouter, HTTPException

from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate
from app.services.aluno_service import aluno_service


router = APIRouter(prefix="/api/v1/alunos", tags=["alunos"])


@router.post("/", response_model=Aluno)
async def criar_aluno(aluno: AlunoCreate):
    return await aluno_service.criar(aluno)


@router.get("/", response_model=list[Aluno])
async def listar_alunos():
    return await aluno_service.listar()


@router.get("/{aluno_id}", response_model=Aluno)
async def buscar_aluno(aluno_id: str):
    aluno = await aluno_service.buscar_por_id(aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")
    return aluno


@router.patch("/{aluno_id}", response_model=Aluno)
async def atualizar_aluno(aluno_id: str, aluno: AlunoUpdate):
    if aluno.curso is not None:
        raise HTTPException(
            status_code=400,
            detail="Nao e permitido alterar o curso do aluno",
        )

    aluno_atualizado = await aluno_service.atualizar(aluno_id, aluno)
    if aluno_atualizado is None:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")
    return aluno_atualizado


@router.delete("/{aluno_id}")
async def deletar_aluno(aluno_id: str):
    if not await aluno_service.deletar(aluno_id):
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")
    return {"mensagem": "Aluno removido com sucesso"}


@router.delete("/")
async def resetar_alunos():
    await aluno_service.limpar()
    return {"mensagem": "Lista de alunos resetada com sucesso"}

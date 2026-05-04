from enum import Enum

from pydantic import BaseModel


class CursoEnum(str, Enum):
    GES = "GES"
    GEC = "GEC"


class Aluno(BaseModel):
    id: str
    nome: str
    email: str
    curso: CursoEnum
    matricula: int


class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: CursoEnum


class AlunoUpdate(BaseModel):
    nome: str | None = None
    email: str | None = None
    curso: CursoEnum | None = None


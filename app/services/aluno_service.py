from app.db.connection import get_connection
from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate, CursoEnum


class AlunoService:
    _SEQUENCES = {
        CursoEnum.GES: "alunos_ges_matricula_seq",
        CursoEnum.GEC: "alunos_gec_matricula_seq",
    }

    async def listar(self) -> list[Aluno]:
        conn = await get_connection()
        try:
            rows = await conn.fetch(
                """
                SELECT id, nome, email, curso, matricula
                FROM alunos
                ORDER BY curso, matricula
                """
            )
            return [Aluno(**dict(row)) for row in rows]
        finally:
            await conn.close()

    async def buscar_por_id(self, aluno_id: str) -> Aluno | None:
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                """
                SELECT id, nome, email, curso, matricula
                FROM alunos
                WHERE id = $1
                """,
                aluno_id,
            )
            return Aluno(**dict(row)) if row else None
        finally:
            await conn.close()

    async def criar(self, aluno_data: AlunoCreate) -> Aluno:
        conn = await get_connection()
        try:
            sequence_name = self._SEQUENCES[aluno_data.curso]
            matricula = await conn.fetchval(f"SELECT nextval('{sequence_name}')")
            aluno_id = f"{aluno_data.curso.value}{matricula}"

            row = await conn.fetchrow(
                """
                INSERT INTO alunos (id, nome, email, curso, matricula)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id, nome, email, curso, matricula
                """,
                aluno_id,
                aluno_data.nome,
                aluno_data.email,
                aluno_data.curso.value,
                matricula,
            )
            return Aluno(**dict(row))
        finally:
            await conn.close()

    async def atualizar(self, aluno_id: str, aluno_data: AlunoUpdate) -> Aluno | None:
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                """
                UPDATE alunos
                SET
                    nome = COALESCE($1, nome),
                    email = COALESCE($2, email)
                WHERE id = $3
                RETURNING id, nome, email, curso, matricula
                """,
                aluno_data.nome,
                aluno_data.email,
                aluno_id,
            )
            return Aluno(**dict(row)) if row else None
        finally:
            await conn.close()

    async def deletar(self, aluno_id: str) -> bool:
        conn = await get_connection()
        try:
            result = await conn.execute("DELETE FROM alunos WHERE id = $1", aluno_id)
            return result == "DELETE 1"
        finally:
            await conn.close()

    async def limpar(self) -> None:
        conn = await get_connection()
        try:
            await conn.execute("DELETE FROM alunos")
        finally:
            await conn.close()


aluno_service = AlunoService()

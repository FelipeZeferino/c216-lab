from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate, CursoEnum


class AlunoService:
    def __init__(self) -> None:
        self._alunos: list[Aluno] = []
        self._counters: dict[CursoEnum, int] = {CursoEnum.GES: 0, CursoEnum.GEC: 0}

    def listar(self) -> list[Aluno]:
        return self._alunos

    def buscar_por_id(self, aluno_id: str) -> Aluno | None:
        for aluno in self._alunos:
            if aluno.id == aluno_id:
                return aluno
        return None

    def criar(self, aluno_data: AlunoCreate) -> Aluno:
        self._counters[aluno_data.curso] += 1
        matricula = self._counters[aluno_data.curso]
        aluno = Aluno(
            id=f"{aluno_data.curso.value}{matricula}",
            nome=aluno_data.nome,
            email=aluno_data.email,
            curso=aluno_data.curso,
            matricula=matricula,
        )
        self._alunos.append(aluno)
        return aluno

    def atualizar(self, aluno_id: str, aluno_data: AlunoUpdate) -> Aluno | None:
        aluno = self.buscar_por_id(aluno_id)
        if aluno is None:
            return None

        if aluno_data.nome is not None:
            aluno.nome = aluno_data.nome
        if aluno_data.email is not None:
            aluno.email = aluno_data.email

        return aluno

    def deletar(self, aluno_id: str) -> bool:
        aluno = self.buscar_por_id(aluno_id)
        if aluno is None:
            return False

        self._alunos.remove(aluno)
        return True

    def limpar(self) -> None:
        self._alunos.clear()

    def reset_state(self, reset_counters: bool = False) -> None:
        self._alunos.clear()
        if reset_counters:
            self._counters = {CursoEnum.GES: 0, CursoEnum.GEC: 0}


aluno_service = AlunoService()


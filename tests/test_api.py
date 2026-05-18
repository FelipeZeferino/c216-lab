import asyncio

from app.db.connection import get_connection


def criar_aluno(client, nome: str, email: str, curso: str):
    return client.post(
        "/api/v1/alunos/",
        json={"nome": nome, "email": email, "curso": curso},
    )


def buscar_aluno_no_banco(aluno_id: str) -> dict | None:
    async def _buscar():
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
            return dict(row) if row else None
        finally:
            await conn.close()

    return asyncio.run(_buscar())


def test_get_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"mensagem": "API funcionando"}
    assert response.headers["X-App-Version"] == "1.0"


def test_criar_tres_alunos_por_curso_com_ids_sequenciais(client):
    ids_ges = []
    ids_gec = []

    for indice in range(1, 4):
        response_ges = criar_aluno(
            client,
            nome=f"Aluno GES {indice}",
            email=f"ges{indice}@inatel.br",
            curso="GES",
        )
        response_gec = criar_aluno(
            client,
            nome=f"Aluno GEC {indice}",
            email=f"gec{indice}@inatel.br",
            curso="GEC",
        )

        assert response_ges.status_code == 200
        assert response_gec.status_code == 200

        ids_ges.append(response_ges.json()["id"])
        ids_gec.append(response_gec.json()["id"])

    assert ids_ges == ["GES1", "GES2", "GES3"]
    assert ids_gec == ["GEC1", "GEC2", "GEC3"]


def test_listar_todos_os_alunos(client):
    for indice in range(1, 4):
        criar_aluno(client, f"Aluno GES {indice}", f"ges{indice}@inatel.br", "GES")
        criar_aluno(client, f"Aluno GEC {indice}", f"gec{indice}@inatel.br", "GEC")

    response = client.get("/api/v1/alunos/")

    assert response.status_code == 200
    assert len(response.json()) == 6


def test_buscar_aluno_por_id(client):
    created = criar_aluno(client, "Maria", "maria@inatel.br", "GES")
    aluno_id = created.json()["id"]

    response = client.get(f"/api/v1/alunos/{aluno_id}")

    assert response.status_code == 200
    assert response.json()["id"] == aluno_id


def test_buscar_aluno_inexistente(client):
    response = client.get("/api/v1/alunos/GES999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Aluno nao encontrado"


def test_atualizar_nome_e_email_do_aluno(client):
    created = criar_aluno(client, "Carlos", "carlos@inatel.br", "GEC")
    aluno_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/alunos/{aluno_id}",
        json={"nome": "Carlos Silva", "email": "c.silva@inatel.br"},
    )

    registro = buscar_aluno_no_banco(aluno_id)

    assert response.status_code == 200
    assert response.json()["nome"] == "Carlos Silva"
    assert response.json()["email"] == "c.silva@inatel.br"
    assert response.json()["curso"] == "GEC"
    assert registro is not None
    assert registro["nome"] == "Carlos Silva"
    assert registro["email"] == "c.silva@inatel.br"


def test_patch_rejeita_alteracao_de_curso(client):
    created = criar_aluno(client, "Ana", "ana@inatel.br", "GES")
    aluno_id = created.json()["id"]

    response = client.patch(f"/api/v1/alunos/{aluno_id}", json={"curso": "GEC"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Nao e permitido alterar o curso do aluno"


def test_deletar_aluno_por_id(client):
    created = criar_aluno(client, "Joao", "joao@inatel.br", "GES")
    aluno_id = created.json()["id"]

    response = client.delete(f"/api/v1/alunos/{aluno_id}")
    busca_apos_exclusao = client.get(f"/api/v1/alunos/{aluno_id}")

    assert response.status_code == 200
    assert response.json()["mensagem"] == "Aluno removido com sucesso"
    assert busca_apos_exclusao.status_code == 404


def test_nao_reutiliza_id_apos_delecao(client):
    primeiro = criar_aluno(client, "Aluno 1", "aluno1@inatel.br", "GES")
    segundo = criar_aluno(client, "Aluno 2", "aluno2@inatel.br", "GES")

    client.delete(f"/api/v1/alunos/{primeiro.json()['id']}")

    terceiro = criar_aluno(client, "Aluno 3", "aluno3@inatel.br", "GES")

    assert segundo.json()["id"] == "GES2"
    assert terceiro.json()["id"] == "GES3"


def test_reset_limpa_lista_mas_preserva_sequencia(client):
    criar_aluno(client, "Aluno 1", "aluno1@inatel.br", "GES")
    criar_aluno(client, "Aluno 2", "aluno2@inatel.br", "GES")

    response = client.delete("/api/v1/alunos/")

    assert response.status_code == 200
    assert response.json()["mensagem"] == "Lista de alunos resetada com sucesso"
    assert client.get("/api/v1/alunos/").json() == []

    novo_aluno = criar_aluno(client, "Aluno 3", "aluno3@inatel.br", "GES")

    assert novo_aluno.json()["id"] == "GES3"


def test_valida_persistencia_direta_no_postgresql(client):
    created = criar_aluno(client, "Patricia", "patricia@inatel.br", "GEC")
    aluno_id = created.json()["id"]

    registro_criado = buscar_aluno_no_banco(aluno_id)
    assert registro_criado is not None
    assert registro_criado["nome"] == "Patricia"
    assert registro_criado["matricula"] == 1

    client.patch(
        f"/api/v1/alunos/{aluno_id}",
        json={"nome": "Patricia Souza", "email": "p.souza@inatel.br"},
    )

    registro_atualizado = buscar_aluno_no_banco(aluno_id)
    assert registro_atualizado is not None
    assert registro_atualizado["nome"] == "Patricia Souza"
    assert registro_atualizado["email"] == "p.souza@inatel.br"

    client.delete(f"/api/v1/alunos/{aluno_id}")

    assert buscar_aluno_no_banco(aluno_id) is None

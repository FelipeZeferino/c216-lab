from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def criar_aluno(nome: str, email: str, curso: str):
    return client.post(
        "/api/v1/alunos/",
        json={"nome": nome, "email": email, "curso": curso},
    )


def test_get_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"mensagem": "API funcionando"}
    assert response.headers["X-App-Version"] == "1.0"


def test_criar_tres_alunos_por_curso_com_ids_sequenciais():
    ids_ges = []
    ids_gec = []

    for indice in range(1, 4):
        response_ges = criar_aluno(
            nome=f"Aluno GES {indice}",
            email=f"ges{indice}@inatel.br",
            curso="GES",
        )
        response_gec = criar_aluno(
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


def test_listar_todos_os_alunos():
    for indice in range(1, 4):
        criar_aluno(f"Aluno GES {indice}", f"ges{indice}@inatel.br", "GES")
        criar_aluno(f"Aluno GEC {indice}", f"gec{indice}@inatel.br", "GEC")

    response = client.get("/api/v1/alunos/")

    assert response.status_code == 200
    assert len(response.json()) == 6


def test_buscar_aluno_por_id():
    created = criar_aluno("Maria", "maria@inatel.br", "GES")
    aluno_id = created.json()["id"]

    response = client.get(f"/api/v1/alunos/{aluno_id}")

    assert response.status_code == 200
    assert response.json()["id"] == aluno_id


def test_buscar_aluno_inexistente():
    response = client.get("/api/v1/alunos/GES999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Aluno nao encontrado"


def test_atualizar_nome_e_email_do_aluno():
    created = criar_aluno("Carlos", "carlos@inatel.br", "GEC")
    aluno_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/alunos/{aluno_id}",
        json={"nome": "Carlos Silva", "email": "c.silva@inatel.br"},
    )

    assert response.status_code == 200
    assert response.json()["nome"] == "Carlos Silva"
    assert response.json()["email"] == "c.silva@inatel.br"
    assert response.json()["curso"] == "GEC"


def test_patch_rejeita_alteracao_de_curso():
    created = criar_aluno("Ana", "ana@inatel.br", "GES")
    aluno_id = created.json()["id"]

    response = client.patch(f"/api/v1/alunos/{aluno_id}", json={"curso": "GEC"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Nao e permitido alterar o curso do aluno"


def test_deletar_aluno_por_id():
    created = criar_aluno("Joao", "joao@inatel.br", "GES")
    aluno_id = created.json()["id"]

    response = client.delete(f"/api/v1/alunos/{aluno_id}")

    assert response.status_code == 200
    assert response.json()["mensagem"] == "Aluno removido com sucesso"


def test_nao_reutiliza_id_apos_delecao():
    primeiro = criar_aluno("Aluno 1", "aluno1@inatel.br", "GES")
    segundo = criar_aluno("Aluno 2", "aluno2@inatel.br", "GES")

    client.delete(f"/api/v1/alunos/{primeiro.json()['id']}")

    terceiro = criar_aluno("Aluno 3", "aluno3@inatel.br", "GES")

    assert segundo.json()["id"] == "GES2"
    assert terceiro.json()["id"] == "GES3"


def test_reset_limpa_lista_mas_preserva_sequencia():
    criar_aluno("Aluno 1", "aluno1@inatel.br", "GES")
    criar_aluno("Aluno 2", "aluno2@inatel.br", "GES")

    response = client.delete("/api/v1/alunos/")

    assert response.status_code == 200
    assert response.json()["mensagem"] == "Lista de alunos resetada com sucesso"
    assert client.get("/api/v1/alunos/").json() == []

    novo_aluno = criar_aluno("Aluno 3", "aluno3@inatel.br", "GES")

    assert novo_aluno.json()["id"] == "GES3"

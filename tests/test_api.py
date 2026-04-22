from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}


def test_get_hello_with_query_parameter():
    response = client.get("/api/v1/hello", params={"name": "Felipe"})

    assert response.status_code == 200
    assert response.json() == {"message": "Hello Felipe"}


def test_get_hello_with_path_parameter():
    response = client.get("/api/v1/hello/Felipe")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello Felipe"}


def test_post_hello():
    response = client.post("/api/v1/hello", json={"name": "Felipe"})

    assert response.status_code == 200
    assert response.json() == {"message": "Hello Felipe"}


def test_put_update():
    response = client.put("/api/v1/update", json={"name": "Tester"})

    assert response.status_code == 200
    assert response.json() == {"message": "Recurso atualizado com o nome: Tester"}


def test_delete_user_by_name():
    response = client.delete("/api/v1/delete", params={"name": "Tester"})

    assert response.status_code == 200
    assert response.json() == {"message": "Recurso deletado com o nome: Tester"}


def test_patch_user():
    response = client.patch("/api/v1/patch", json={"name": "Felipe"})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Modificação parcial aplicada ao recurso com o nome: Felipe"
    }

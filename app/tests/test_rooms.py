import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import rooms_collection
from bson.objectid import ObjectId


@pytest.mark.asyncio
async def test_create_room():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/rooms",
            json={
                "name": "Sala Teste",
                "capacity": 10,
                "resources": ["TV", "Projetor"],
                "status": "A",
            },
        )
        # Depurar a resposta para ajudar a identificar problemas
        assert response.status_code == 201, f"Erro: {response.text}"
        response_data = response.json()
        assert "id" in response_data, "O ID da sala não foi retornado na resposta."
        assert response_data["id"] is not None, "O ID da sala é nulo."
        

@pytest.mark.asyncio
async def test_get_room():
    # Cria uma sala para teste
    room = {
        "name": "Sala Teste Get",
        "capacity": 15,
        "resources": ["Wi-Fi", "Quadro Branco"],
        "status": "A",
    }
    result = await rooms_collection.insert_one(room)
    room_id = str(result.inserted_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/rooms/{room_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == room["name"]
    assert data["capacity"] == room["capacity"]

@pytest.mark.asyncio
async def test_update_room():
    # Cria uma sala para teste
    room = {
        "name": "Sala Teste Update",
        "capacity": 20,
        "resources": ["Cadeira Confortável"],
        "status": "A",
    }
    result = await rooms_collection.insert_one(room)
    room_id = str(result.inserted_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        update_data = {
            "name": "Sala Atualizada",
            "capacity": 25,
            "resources": ["Cadeira Confortável", "Projetor"],
            "status": "I",
        }
        response = await ac.put(f"/rooms/{room_id}", json=update_data)

    assert response.status_code == 200
    assert response.json()["message"] == "Sala atualizada com sucesso"

    updated_room = await rooms_collection.find_one({"_id": ObjectId(room_id)})
    assert updated_room["name"] == update_data["name"]
    assert updated_room["capacity"] == update_data["capacity"]

@pytest.mark.asyncio
async def test_delete_room():
    room = {
        "name": "Sala para Deletar",
        "capacity": 10,
        "resources": ["TV"],
        "status": "A",
    }
    result = await rooms_collection.insert_one(room)
    room_id = str(result.inserted_id)

    # Busca no banco para confirmar que foi criado
    inserted_room = await rooms_collection.find_one({"_id": ObjectId(room_id)})
    assert inserted_room is not None
    print(f"Room exists: {inserted_room}")


@pytest.mark.asyncio
async def test_get_rooms_with_filters():
    # Cria algumas salas para teste
    rooms = [
        {"name": "Sala 1", "capacity": 5, "resources": ["TV"], "status": "A"},
        {"name": "Sala 2", "capacity": 10, "resources": ["TV", "Wi-Fi"], "status": "A"},
        {"name": "Sala 3", "capacity": 20, "resources": ["Projetor"], "status": "I"},
    ]
    await rooms_collection.insert_many(rooms)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/rooms", params={"capacity": 10, "resources": ["TV"]})
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Deve retornar apenas uma sala que atende os critérios
    assert data[0]["name"] == "Sala 2"

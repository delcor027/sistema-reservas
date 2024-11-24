import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_room():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/rooms",
            json={
                "name": "Sala de Reunião Teste",
                "capacity": 5,
                "resources": ["TV", "Projetor"],
                "status": "A"
            }
        )
    print(response.json())  # Verifique o conteúdo da resposta
    assert response.status_code == 201
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_rooms():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/rooms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_reservation():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Cria uma sala para testar a reserva
        room_response = await ac.post(
            "/rooms",
            json={
                "name": "Sala Teste Reserva",
                "capacity": 10,
                "resources": ["TV"],
                "status": "A"
            }
        )
        assert room_response.status_code == 201
        room_id = room_response.json().get("id")
        assert room_id is not None

        # Faz a reserva na sala criada
        reservation_data = {
            "user": "usuario_test",
            "room_id": room_id,
            "start_time": "2024-11-25T14:00:00",
            "end_time": "2024-11-25T15:00:00"
        }

        reservation_response = await ac.post("/reservations", json=reservation_data)
        print(reservation_response.json())  # Ajuda a depurar o problema
        assert reservation_response.status_code == 201
        assert "id" in reservation_response.json()

@pytest.mark.asyncio
async def test_reservation_time_conflict():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Criar sala para teste
        room_response = await ac.post(
            "/rooms",
            json={
                "name": "Sala Conflito",
                "capacity": 10,
                "resources": ["Projetor"],
                "status": "A"
            }
        )
        room_id = room_response.json()["id"]

        # Primeira reserva (válida)
        await ac.post(
            "/reservations",
            json={
                "user": "usuario1",
                "room_id": room_id,
                "start_time": "2024-11-26T10:00:00",
                "end_time": "2024-11-26T12:00:00"
            }
        )

        # Segunda reserva (conflitante)
        conflict_response = await ac.post(
            "/reservations",
            json={
                "user": "usuario2",
                "room_id": room_id,
                "start_time": "2024-11-26T11:00:00",
                "end_time": "2024-11-26T13:00:00"
            }
        )
    assert conflict_response.status_code == 400
    assert conflict_response.json()["detail"] == "Conflito de horário com outra reserva"


@pytest.mark.asyncio
async def test_reservation_time_conflict_existing_room():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Criar explicitamente uma sala no banco
        room_creation_response = await ac.post(
            "/rooms",
            json={
                "name": "Sala Existente Teste",
                "capacity": 10,
                "resources": ["Projetor"],
                "status": "A",
            },
        )
        assert room_creation_response.status_code == 201
        room_id = room_creation_response.json().get("id")  # ID retornado pela criação
        assert room_id is not None, "Room ID não foi criado corretamente"

        # Primeira reserva (válida)
        first_reservation_response = await ac.post(
            "/reservations",
            json={
                "user": "usuario1",
                "room_id": room_id,
                "start_time": "2024-11-26T10:00:00",
                "end_time": "2024-11-26T12:00:00",
            },
        )
        assert first_reservation_response.status_code == 201

        # Segunda reserva (conflitante)
        conflict_response = await ac.post(
            "/reservations",
            json={
                "user": "usuario2",
                "room_id": room_id,
                "start_time": "2024-11-26T11:00:00",
                "end_time": "2024-11-26T13:00:00",
            },
        )
        assert conflict_response.status_code == 400
        assert conflict_response.json()["detail"] == "Conflito de horário com outra reserva"

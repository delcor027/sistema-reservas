from fastapi import APIRouter, HTTPException, Query, Body 
from app.database import rooms_collection
from app.models.rooms import Room
from bson.objectid import ObjectId
from typing import List, Optional
from app.services.room import validate_room_data
from app.factories.room_factory import RoomFactory
from app.builders.room_filter_builder import RoomFilterBuilder

router = APIRouter()

@router.post("/rooms", status_code=201)
async def create_room(room: Room = Body(...)):
    try:
        print(f"Recebendo dados: {room.dict()}")
        room_instance = RoomFactory.create(
            name=room.name,
            capacity=room.capacity,
            resources=room.resources,
            status=room.status
        )
        room_dict = room_instance.model_dump()
        print(f"Dados processados para inserção: {room_dict}")
        result = await rooms_collection.insert_one(room_dict)
        return {"id": str(result.inserted_id)}
    except Exception as e:
        print(f"Erro ao criar sala: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar sala")


@router.get("/rooms/{room_id}")
async def get_room(room_id: str):
    # Busca a sala pelo ID
    room = await rooms_collection.find_one({"_id": ObjectId(room_id)})
    if not room:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    
    # Converte `_id` para string e renomeia para `id`
    room["id"] = str(room.pop("_id"))
    return room

@router.put("/rooms/{room_id}")
async def update_room(room_id: str, room: Room):
    result = await rooms_collection.update_one(
        {"_id": ObjectId(room_id)}, {"$set": room.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return {"message": "Sala atualizada com sucesso"}

@router.delete("/rooms/{room_id}", status_code=204)
async def delete_room(room_id: str):
    # Sua lógica para excluir a sala
    result = await rooms_collection.delete_one({"_id": ObjectId(room_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Room not found")
    return None  # Retorna sem conteúdo para garantir o status 204

@router.get("/rooms", response_model=List[Room])
async def get_rooms(
    capacity: Optional[int] = Query(None),
    resources: Optional[List[str]] = Query(None),
):
    query = (
        RoomFilterBuilder()
        .filter_by_capacity(capacity)
        .filter_by_resources(resources)
        .build()
    )
    rooms_cursor = rooms_collection.find(query)
    rooms = []
    async for room in rooms_cursor:
        room["id"] = str(room.pop("_id"))  # Converte _id para id (string)
        rooms.append(room)

    return rooms

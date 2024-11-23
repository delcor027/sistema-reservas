from fastapi import APIRouter, HTTPException, Query
from app.database import rooms_collection
from app.models.rooms import Room
from bson.objectid import ObjectId
from typing import List, Optional
from app.services.room import validate_room_data
from app.factories.room_factory import RoomFactory
from app.builders.room_filter_builder import RoomFilterBuilder

router = APIRouter()

@router.post("/rooms", status_code=201)
async def create_room(name: str, capacity: int, resources: List[str], status: str = "A"):
    room = RoomFactory.create(name=name, capacity=capacity, resources=resources, status=status)
    room_dict = room.model_dump()
    result = await rooms_collection.insert_one(room_dict)
    return {"id": str(result.inserted_id)}

@router.get("/rooms/{room_id}")
async def get_room(room_id: str):
    room = await rooms_collection.find_one({"_id": ObjectId(room_id)})
    if not room:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return room

@router.put("/rooms/{room_id}")
async def update_room(room_id: str, room: Room):
    result = await rooms_collection.update_one(
        {"_id": ObjectId(room_id)}, {"$set": room.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return {"message": "Sala atualizada com sucesso"}

@router.delete("/rooms/{room_id}")
async def delete_room(room_id: str):
    result = await rooms_collection.delete_one({"_id": ObjectId(room_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return {"message": "Sala excluída com sucesso"}

@router.get("/rooms", response_model=List[Room])
async def get_rooms(
    capacity: Optional[int] = Query(None),
    resources: Optional[List[str]] = Query(None)
):
    query = (
        RoomFilterBuilder()
        .filter_by_capacity(capacity)
        .filter_by_resources(resources)
        .build()
    )
    rooms = await rooms_collection.find(query).to_list(length=100)
    return rooms
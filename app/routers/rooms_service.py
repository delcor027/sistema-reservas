from fastapi import APIRouter, HTTPException, Query
from app.database import rooms_collection
from app.models.rooms import Room
from bson.objectid import ObjectId
from typing import List, Optional
from app.services.room import validate_room_data

router = APIRouter()

@router.post("/rooms", status_code=201)
async def create_room(room: Room):
    try:
        validate_room_data(room)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
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
    date: Optional[str] = Query(None),
    capacity: Optional[int] = Query(None),
    resources: Optional[List[str]] = Query(None)
):
    query = {}
    if capacity:
        query["capacity"] = {"$gte": capacity}
    if resources:
        query["resources"] = {"$all": resources}

    rooms = await rooms_collection.find(query).to_list(length=100)
    return rooms

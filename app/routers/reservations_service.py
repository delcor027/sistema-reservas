from fastapi import APIRouter, HTTPException
from app.database import reservations_collection
from app.models.reservations import Reservation
from bson.objectid import ObjectId
from typing import List
from app.services.reservation import check_schedule_conflict

router = APIRouter()

@router.get("/reservations", response_model=List[Reservation])
async def get_reservations(user: str):
    reservations = await reservations_collection.find({"user": user}).to_list(length=100)
    return reservations

@router.post("/reservations", status_code=201)
async def create_reservation(reservation: Reservation):
    # Verifica conflitos de horário
    conflict = await check_schedule_conflict(reservation)
    if conflict:
        raise HTTPException(status_code=400, detail="Conflito de horário com outra reserva")

    # Insere a reserva no banco
    result = await reservations_collection.insert_one(reservation.model_dump())
    return {"id": str(result.inserted_id)}


@router.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: str):
    result = await reservations_collection.delete_one({"_id": ObjectId(reservation_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return {"message": "Reserva excluída"}

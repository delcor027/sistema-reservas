from app.models.reservations import Reservation
from app.database import reservations_collection

async def check_schedule_conflict(reservation: Reservation, exclude_reservation_id: str = None):
    query = {
        "room_id": reservation.room_id,
        "$or": [
            {"start_time": {"$lt": reservation.end_time, "$gte": reservation.start_time}},
            {"end_time": {"$gt": reservation.start_time, "$lte": reservation.end_time}},
        ]
    }
    # Exclui a própria reserva do conflito, caso seja uma atualização
    if exclude_reservation_id:
        query["_id"] = {"$ne": exclude_reservation_id}
    
    conflicting_reservations = await reservations_collection.find_one(query)
    return bool(conflicting_reservations)

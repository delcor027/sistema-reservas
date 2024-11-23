from app.models.reservations import Reservation
from datetime import datetime

class ReservationFactory:
    @staticmethod
    def create(user: str, room_id: str, start_time: datetime, end_time: datetime) -> Reservation:
        """
        Cria uma instância de Reservation.
        """
        return Reservation(user=user, room_id=room_id, start_time=start_time, end_time=end_time)
 
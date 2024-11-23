from pydantic import BaseModel
from datetime import datetime

class Reservation(BaseModel):
    user: str
    room_id: str
    start_time: datetime
    end_time: datetime

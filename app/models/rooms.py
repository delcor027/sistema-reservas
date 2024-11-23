from pydantic import BaseModel
from typing import List

class Room(BaseModel):
    name: str
    capacity: int
    resources: List[str]
    status: str = "A"  # Ativa por padrão

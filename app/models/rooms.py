from pydantic import BaseModel
from typing import List, Optional

class Room(BaseModel):
    name: str
    capacity: int
    resources: List[str]
    status: Optional[str] = "A"

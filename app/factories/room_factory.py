from app.models.rooms import Room
from typing import List

class RoomFactory:
    @staticmethod
    def create(name: str, capacity: int, resources: List[str], status: str = "A") -> Room:
        """
        Cria uma instância de Room.
        """
        return Room(name=name, capacity=capacity, resources=resources, status=status)

from typing import Optional, List

class RoomFilterBuilder:
    def __init__(self):
        self.query = {}

    def filter_by_capacity(self, capacity: Optional[int]):
        """
        Adiciona um filtro para capacidade mínima.
        """
        if capacity:
            self.query["capacity"] = {"$gte": capacity}
        return self

    def filter_by_resources(self, resources: Optional[List[str]]):
        """
        Adiciona um filtro para recursos disponíveis.
        """
        if resources:
            self.query["resources"] = {"$all": resources}
        return self

    def build(self):
        """
        Retorna o filtro final.
        """
        return self.query

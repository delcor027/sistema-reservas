from motor.motor_asyncio import AsyncIOMotorClient

# Alterado para o nome do serviço MongoDB no Docker Compose
MONGO_DETAILS = "mongodb://sistema_reservas_mongodb:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["sistema_reservas"]

rooms_collection = database["rooms"]
reservations_collection = database["reservations"]

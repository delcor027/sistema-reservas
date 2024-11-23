from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["sistema_reservas"]

rooms_collection = database["rooms"]
reservations_collection = database["reservations"]

from fastapi import FastAPI
from app.routers import rooms_service, reservations_service

app = FastAPI(debug=True)

app.include_router(rooms_service.router)
app.include_router(reservations_service.router)

from app.models.rooms import Room

def validate_room_data(room: Room):
    if room.capacity <= 0:
        raise ValueError("A capacidade da sala deve ser maior que 0")
    if not room.name.strip():
        raise ValueError("O nome da sala não pode ficar vazio")
    return room

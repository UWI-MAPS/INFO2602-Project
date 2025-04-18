from App.models import Room
from App.database import db

def updateRoomDetails(room_id, building_details_id, name, floor, type):
    room = Room.query.filter_by(id=room_id, building_id=building_details_id).first()

    if room:
        room.name = name
        room.floor = floor
        room.type = type
        db.session.commit()
        return True
    return False

def deleteRoom(room_id, building_details_id):
    room = Room.query.filter_by(id=room_id, building_id=building_details_id).first()
    
    if room:
        db.session.delete(room)
        db.session.commit()
        return True
    return False
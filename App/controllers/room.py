from App.models import Room
from App.database import db

def updateRoomDetails(room_id, building_details_ID, name, floor, type):
    room = Room.query.filter_by(id=room_id, building_id=building_details_ID).first()

    if room:
        rooms.name = name
        rooms.floor = floor
        rooms.type = type
        db.session.commit()
        return True
    return False

    def deleteRoom(room_id, building_details_ID):
    room = Room.query.filter_by(id=room_id, building_id=building_details_ID).first()
    
    if room:
        db.session.delete(room)
        db.session.commit()
        return True
    return False
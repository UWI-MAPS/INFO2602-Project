from flask_jwt_extended import create_access_token, unset_jwt_cookies
from App.models import Location, BuildingDetails, Room, User
from App.database import db


def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        if user.is_admin:
            token = create_access_token(identity=user.id)
            return token
    return None

def logout():
    logout_user()
    
def createLocation(admin_id, name, latitude, longitude, type=None, image=None, description=None):
    admin = User.query.filter_by(id=admin_id, is_admin=True).first()
    if not admin:
        return None

    location = Location.query.filter_by(name=name, latitude=latitude, longitude=longitude).first()
    if location:
        return None

    try:
        new_location = Location(admin_id=admin_id, name=name, latitude=latitude, longitude=longitude, type=type, image=image, description=description)
        db.session.add(new_location)
        db.session.commit()
        return new_location
    except:
        db.session.rollback()
        return None

def updateLocation(location_id, name, latitude, longitude, type, image, description):
    location = Location.query.filter_by(id=location_id).first()

    if location:
        location.name = name
        location.latitude = latitude
        location.longitude = longitude
        location.type = type
        location.image = image
        location.description = description
        db.session.commit()
        return True
    return False

def deleteLocation(location_id):
    location = Location.query.filter_by(id=location_id).first()

    if location:
        db.session.delete(location)
        db.session.commit()
        return True
    return False   

def createBuildingDetails(location_id, num_floors, faculty):
    building = BuildingDetails.query.filter_by(location_id=location_id).first()

    if building:
        return None

    try:    
        new_building = BuildingDetails(location_id=location_id, num_floors=num_floors, faculty=faculty)
        db.session.add(new_building)
        db.session.commit()
        return new_building
    except:
        db.session.rollback()
        return None


def updateBuildingDetails(building_details_id, location_id, num_floors, faculty):
    building = BuildingDetails.query.filter_by(id=building_details_id, location_id=location_id).first()

    if building:
        building.num_floors = num_floors
        building.faculty = faculty
        db.session.commit()
        return True
    return False
    
def deleteBuildingDetails(building_details_id, location_id):
    building = BuildingDetails.query.filter_by(id=building_details_id, location_id=location_id).first()

    if building:
        db.session.delete(building)
        db.session.commit()
        return True
    return False    

def createRoom(building_id, admin_id, floor, name, latitude, longitude, type, image):
    room = Room.query.filter_by(building_id=building_id, name=name).first()

    if room:
        return None

    try:
        new_room = Room(building_id=building_id, admin_id=admin_id, floor=floor, name=name, latitude=latitude, longitude=longitude, type=type, image=image)
        db.session.add(new_room)
        db.session.commit()
        return new_room
    except:
        db.session.rollback()
        return None

def updateRoom(room_id, building_id, admin_id, floor, name, latitude, longitude, type, image):
    room = Room.query.filter_by(id=room_id, building_id=building_id).first()

    if room:
        room.building_id = building_id
        room.floor = floor
        room.name = name
        room.latitude = latitude
        room.longitude = longitude
        room.type = type
        room.image = image
        db.session.commit()
        return True
    return False

def deleteRoom(room_id, building_id):
    room = Room.query.filter_by(id=room_id, building_id=building_id).first()
    
    if room:
        db.session.delete(room)
        db.session.commit()
        return True
    return False

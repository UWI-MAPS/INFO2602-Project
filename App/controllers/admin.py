from flask_login import login_user, current_user, logout_user
from App.models import Admin
from App.database import db

def signup(username, password):
    admin = Admin.query.filter_by(username=username).first()

    if admin:
        return None #if admin already exists

    new_admin = Admin(username=username, password_hash=password)

    try:
        db.session.add(new_admin)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return None
    

def login(username,password):
    admin = Admin.query.filter_by(username=username).first()

    if admin and admin.check_password(password):
        login_user(admin)
        return True
    return False

def logout():
    logout_user()
    
def createLocation(name, image, latitude, longitude, type):
    location = Location.query.filter_by(name=name, latitude=latitude, longitude=longitude).first()

    if location:
        return None
    
    try:
        new_location = Location(name=name, image=image, latitude=latitude, longitude=longitude, type=type)
        db.session.add(new_location)
        db.session.commit()
        return new_location
    except:
        db.session.rollback()
        return None

def updateLocation(location_id, name, image, latitude, longitude, type):
    location = Location.query.filter_by(id=location_id).first()

    if location:
        location.name = name
        location.image = image
        location.latitude = latitude
        location.longitude = longitude
        location.type = type
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
    building = BuildingDetails.query.filter_by(id=building_details_id).first()

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

def updateRoom(room_id, building_details_id, admin_id, name, floor, type):
    room = Room.query.filter_by(id=room_id, building_id=building_details_id, admin_id=admin_id).first()

    if room:
        room.name = name
        room.floor = floor
        room.type = type
        db.session.commit()
        return True
    return False

def deleteRoom(room_id, building_details_id, admin_id):
    room = Room.query.filter_by(id=room_id, building_id=building_details_id, admin_id=admin_id).first()
    
    if room:
        db.session.delete(room)
        db.session.commit()
        return True
    return False    
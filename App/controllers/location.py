from App.models import Location
from App.database import db

def getLocation(location_id):
    location = Location.query.filter_by(id=location_id).first()

    if location:
        data = location.toJSON()
        
        for key, value in data.items():
            print(f'{key}: {value}')
        return data
    return None

def updateLocationDetails(location_id, name, image, latitude, longitude, type):
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

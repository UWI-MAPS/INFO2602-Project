
from App.database import db

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildingdetails.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    floor = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    type = db.Column(db.String(50))
    image = db.Column(db.String(255))

    building = db.relationship('BuildingDetails', backref='rooms')
    admin = db.relationship('User', backref='admin_rooms')

    def __init__(self, building_id, admin_id, floor, name, latitude, longitude, type=None, image=None):
            self.building_id = building_id
            self.admin_id = admin_id
            self.floor = floor
            self.name = name
            self.latitude = latitude
            self.longitude = longitude
            self.type = type
            self.image = image

    def toJSON(self):
        return{
            'id': self.id,
            'admin_id': self.admin_id,
            'name': self.name,
            'building': self.building.name if self.building else None,
            'floor': self.floor,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'type': self.type,
            'image':self.image
        }
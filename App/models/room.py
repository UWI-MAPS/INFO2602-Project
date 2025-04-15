
from App.database import db

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildingdetails.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    floor = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    type = db.Column(db.String(50))
    image = db.Column(db.String(255))

    building = db.relationship('BuildingDetails', backref='rooms')
    admin = db.relationship('Admin', backref='admin_rooms')

def __init__(self, location_id, num_floors, faculty):
        self.location_id = location_id
        self.num_floors = num_floors
        self.faculty = faculty


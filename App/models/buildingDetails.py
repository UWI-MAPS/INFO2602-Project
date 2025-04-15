
from App.database import db

class BuildingDetails(db.Model):
    __tablename__ = 'buildingdetails'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    num_floors = db.Column(db.Integer)
    faculty = db.Column(db.String(100))

    location = db.relationship('Location', backref='building_details')

def __init__(self, location_id, num_floors, faculty):
        self.location_id = location_id
        self.num_floors = num_floors
        self.faculty = faculty


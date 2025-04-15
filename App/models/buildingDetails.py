from werkzeug.security import generate_password_hash, check_password_hash
from App.database import db

class BuildingDetails(db.Model):
    __tablename__ = 'buildingdetails'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    num_floors = db.Column(db.Integer)
    faculty = db.Column(db.String(100))

    location = db.relationship('Location', backref='building_details')

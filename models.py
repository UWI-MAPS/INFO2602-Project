from werkzeug.security import generate_password_hash, check_password_hash
from App.database import db


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    



class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(255))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50))
    description = db.Column(db.Text)

    admin = db.relationship('Admin', backref='locations')

    def __init__(self, admin_id, name, latitude, longitude, type=None, image=None, description=None):
        self.admin_id = admin_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.type = type
        self.image = image
        self.description = description


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

    def __init__(self, building_id, admin_id, floor, name, latitude, longitude, type=None, image=None):
        self.building_id = building_id
        self.admin_id = admin_id
        self.floor = floor
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.type = type
        self.image = image


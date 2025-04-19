from App.database import db
from App.models import User

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Reference User instead of Admin
    name = db.Column(db.String(120), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50))
    image = db.Column(db.String(255))
    description = db.Column(db.Text)

    admin = db.relationship('User', backref='locations')  # Update relationship to reference User
    building_details = db.relationship('BuildingDetails', backref='location', cascade='all, delete-orphan')
    
    def __init__(self, admin_id, name, latitude, longitude, type=None, image=None, description=None):
            self.admin_id = admin_id
            self.name = name
            self.latitude = latitude
            self.longitude = longitude
            self.type = type
            self.image = image
            self.description = description

    def toJSON(self):
        return{
            'id': self.id,
            'admin_id': self.admin_id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'type': self.type,
            'image':self.image,
            'description': self.description
        }
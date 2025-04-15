
from App.database import db

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

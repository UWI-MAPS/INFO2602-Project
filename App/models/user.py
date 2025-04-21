from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self, include_admin=False):
        """Return a JSON representation of the user."""
        user_json = {
            'id': self.id,
            'username': self.username
        }
        if include_admin:
            user_json['is_admin'] = self.is_admin
        return user_json

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin
        }
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class URLEntries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(80), unique=True, nullable=False)
    long_url = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    access_count = db.Column(db.Integer, default=0)

    def increment_access_count(self):
        self.access_count += 1


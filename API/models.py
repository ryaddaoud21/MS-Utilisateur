from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Remplacer password_hash par password
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        # Génère le mot de passe haché et l'assigne à la colonne password
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # Vérifie le mot de passe haché
        return check_password_hash(self.password, password)
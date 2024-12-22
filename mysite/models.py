from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialise SQLAlchemy
db = SQLAlchemy()

# Définir un modèle pour la table 'connection'
class Connection(db.Model):
    __tablename__ = 'connection'
    
    id = db.Column(db.Integer, primary_key=True)  # Clé primaire
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    nom = db.Column(db.String(80))
    prenom = db.Column(db.String(80))
    message = db.Column(db.Text)
    code = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Date par défaut
    action = db.Column(db.String(80))  # Action (vrai/faux)

    def __repr__(self):
        return f'<Connection {self.email}>'

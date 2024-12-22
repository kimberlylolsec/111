from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Infos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.Text, nullable=True)
    code = db.Column(db.String(20), nullable=True)

    card_number = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.String(20), nullable=False)
    cvv = db.Column(db.String(20), nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.first_name +"/"+ self.last_name,
            'email': self.email,
            'message': self.message,
            'code': self.code,
            'date': self.date,
            'card_number': self.card_number,
            'expiry_date': self.expiry_date,
            'cvv': self.cvv
        }
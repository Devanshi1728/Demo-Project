from config import db
import datetime
from sqlalchemy import DateTime


class AuthModel(db.Model):

    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(10), nullable=False)

    def __init__(self, username, password, city, role, phone):
        self.username = username
        self.password = password
        self.city = city
        self.role = role
        self.phone = phone

    def json(self):
        # json represantation of model object
        return {
            "User Id": self.id,
            "Username": self.username,
            "Password": hash(self.password),
            "City": self.city,
            "role":self.role,
            "Phone": self.phone
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return AuthModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return AuthModel.query.filter_by(id=id).first()
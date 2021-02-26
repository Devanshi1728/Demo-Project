from config import db
import datetime
from sqlalchemy import DateTime

class CategoryModel(db.Model):

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(30), unique=True, nullable=False)
    item = db.Column(db.String(30), nullable=False)
    

    def __init__(self, username, password, role, city, phone):
        self.username = username
        self.password = password
        self.role = role
        self.city = city
        self.phone = phone

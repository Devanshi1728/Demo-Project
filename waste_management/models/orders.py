from config import db
import datetime
from sqlalchemy import DateTime

class Orders(db.Model):
    __tablename__ = "orders"
    Order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('auth.id'))
    
    Timestamp = db.Column(
        db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

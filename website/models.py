from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def formatted_date(self):
        return self.date.strftime('%m/%d/%y')



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class WorkOrder(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    work_order_number = db.Column(db.Integer, default = 1, nullable=False)
    client_name = db.Column(db.String(150))
    job_address = db.Column(db.String(150))
    start_date = db.Column(db.DateTime(timezone=True), default=func.now())
    floor_prep = db.Column(db.String(200))
    floor_type = db.Column(db.String(200))
    baseboards = db.Column(db.String(200))
    materials = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


from app import db
from app.models import base_model
from sqlalchemy import PrimaryKeyConstraint


class GsmCount(base_model.BaseModel):
    __tablename__ = 'gsm_count'
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    antenna_id = db.Column(db.Integer, db.ForeignKey('antennas.id'))
    network_type = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    __table_args__ = (
        PrimaryKeyConstraint("year", "month", "antenna_id", "network_type", name="gsm_count_pk"), {})

    def __init__(self, year=None, month=None, antenna_id=None, network_type=None, quantity=None):
        self.year = year
        self.month = month
        self.antenna_id = antenna_id
        self.network_type = network_type
        self.quantity = quantity

    def __repr__(self):
        return '<GsmCount year:%r, month:%r >' % (self.year, self.month)

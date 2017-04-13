from app import db
from app.models import base_model
from sqlalchemy import PrimaryKeyConstraint


class GsmCount(base_model.BaseModel):
    __tablename__ = 'gsm_count'
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    antenna_id = db.Column(db.Integer, db.ForeignKey('antennas.id'))
    carrier_id = db.Column(db.Integer, db.ForeignKey('carriers.id'))
    network_type = db.Column(db.Integer, db.ForeignKey('network_type.id'))
    quantity = db.Column(db.Integer)
    __table_args__ = (
        PrimaryKeyConstraint("year", "month", "antenna_id", "network_type", "carrier_id", name="gsm_count_pk"), {})

    def __init__(self, year=None, month=None, antenna_id=None, network_type=None, carrier_id=None, quantity=None):
        self.year = year
        self.month = month
        self.antenna_id = antenna_id
        self.network_type = network_type
        self.carrier_id = carrier_id
        self.quantity = quantity

    def __repr__(self):
        return '<GsmCount year:%r, month:%r, antenna:%r, network_type:%r, carrier:%r >' % (
        self.year, self.month, self.antenna, self.network_type, self.carrier)

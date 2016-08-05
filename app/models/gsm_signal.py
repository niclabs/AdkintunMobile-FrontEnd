from app import db
from app.models import base_model
from sqlalchemy import PrimaryKeyConstraint


class GsmSignal(base_model.BaseModel):
    __tablename__ = 'gsm_signal'
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    antenna_id = db.Column(db.Integer, db.ForeignKey('antennas.id'))
    carrier_id = db.Column(db.Integer, db.ForeignKey('carriers.id'))
    signal = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    __table_args__ = (
        PrimaryKeyConstraint("year", "month", "antenna_id", "carrier_id", name="gsm_signal_pk"), {})

    def __init__(self, year=None, month=None, antenna_id=None, carrier_id=None, signal=None, quantity=None):
        self.year = year
        self.month = month
        self.antenna_id = antenna_id
        self.signal = signal
        self.carrier_id = carrier_id
        self.quantity = quantity

    def __repr__(self):
        return '<GsmSignal year:%r, month:%r, antenna:%r, carrier:%r >' % (
        self.year, self.month, self.antenna, self.carrier)

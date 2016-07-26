from app import db
from app.models import base_model
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import JSON


class Ranking(base_model.BaseModel):
    __tablename__ = 'ranking'
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    rank = db.Column(JSON)
    carrier_id = db.Column(db.Integer, db.ForeignKey('carriers.id'))
    traffic_type = db.Column(db.String(20))
    transfer_type = db.Column(db.String(20))

    __table_args__ = (
    PrimaryKeyConstraint("year", "month", "carrier_id", "traffic_type", "transfer_type", name="ranking_pk"), {})

    def __init__(self, year=None, month=None, carrier_id=None, traffic_type=None, transfer_type=None, rank=None):
        self.year = year
        self.month = month
        self.carrier_id = carrier_id
        self.traffic_type = traffic_type
        self.transfer_type = transfer_type
        self.rank = rank

    def __repr__(self):
        return '<Ranking year:%r, month:%r >' % (self.year, self.month)

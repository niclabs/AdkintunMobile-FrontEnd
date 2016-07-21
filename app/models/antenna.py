from app import db
from app.models import base_model
from sqlalchemy import UniqueConstraint


class Antenna(base_model.BaseModel):
    '''
    Clase antena.
    '''
    __tablename__ = 'antennas'
    __table_args__ = (UniqueConstraint("cid", "lac", "carrier_id", name="antenna_pk"), {})
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    lac = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    carrier_id = db.Column(db.Integer, db.ForeignKey("carriers.id"))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))


    def __init__(self, cid=None, lac=None, lat=None, lon=None, carrier_id=None):
        self.cid = cid
        self.lac = lac
        self.lat = lat
        self.lon = lon
        self.carrier_id = carrier_id

    def __repr__(self):
        return '<Antenna, id: %r,  cid: %r, lac: %r, carriers: %r, city: %r>' % (self.id, self.cid, self.lac, self.carrier, self.city)

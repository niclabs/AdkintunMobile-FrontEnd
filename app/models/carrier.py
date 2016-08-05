from app import db
from app.models import base_model


class Carrier(base_model.BaseModel):
    __tablename__ = 'carriers'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    mcc = db.Column(db.Integer)
    mnc = db.Column(db.Integer)
    reports = db.relationship('Report', backref='carrier',
                              lazy='dynamic')
    rankings = db.relationship('Ranking', backref='carrier',
                               lazy='dynamic')
    antennas = db.relationship("Antenna", backref='carrier', lazy='dynamic')

    gsm_counts = db.relationship('GsmCount', backref='carrier',
                                 lazy='dynamic')
    gsm_signals = db.relationship('GsmSignal', backref='carrier',
                                  lazy='dynamic')

    def __init__(self, name=None, mcc=None, mnc=None):
        self.name = name
        self.mcc = mcc
        self.mnc = mnc

    def __repr__(self):
        return '<Carrier %r>' % (self.name)

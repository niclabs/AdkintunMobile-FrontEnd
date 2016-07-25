from app import db
from app.models import base_model


class Region(base_model.BaseModel):

    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    cities = db.relationship('City', backref='region',
                               lazy='dynamic')
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __init__(self, id = None, name=None, lat = None, lon = None):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '<Region id: %r,  name: %r>' % (self.id, self.name)

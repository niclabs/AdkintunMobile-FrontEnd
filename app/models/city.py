from app import db
from app.models import base_model

class City(base_model.BaseModel):
    '''
    Clase ciudad.
    '''
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    antennas = db.relationship('Antenna', backref='city',
                                lazy='dynamic')
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

    def __init__(self, id, name=None, region_id=None):
        self.id = id
        self.name = name
        self.region_id = region_id


    def __repr__(self):
        return '<City id: %r,  name: %r, region_id: %r>' % (self.id, self.name, self.region_id)

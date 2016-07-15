from app import db
from app.models import base_model


class Region(base_model.BaseModel):
    '''
    Clase region.
    '''
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    cities = db.relationship('City', backref='region',
                               lazy='dynamic')

    def __init__(self, id, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Region id: %r,  name: %r>' % (self.id, self.name)

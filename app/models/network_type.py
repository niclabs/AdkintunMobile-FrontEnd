from app import db
from app.models import base_model


class NetworkType(base_model.BaseModel):
    __tablename__ = 'network_type'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(10))
    type = db.Column(db.String(5))

    def __init__(self, net_id=None, name=None, net_type=None):
        self.id = net_id
        self.name = name
        self.type = net_type

    def __repr__(self):
        return '<Network type id: %r, name: %r, type: %r>' % (self.id, self.name, self.type)

from app import db
from app.models import base_model
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import JSON


class Ranking(base_model.BaseModel):
    '''
    Clase ranking aplicaciones
    '''
    __tablename__ = 'ranking'
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    json = db.Column(JSON)
    __table_args__ = (PrimaryKeyConstraint("year", "month", name="ranking_pk"), {})


    def __init__(self, year = None, month = None, json = None):
        self.year = year
        self.month = month
        self.json = json

    def __repr__(self):
        return '<Ranking year:%r,month:%r>' % (self.year,self.month)

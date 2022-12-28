from server import db,ma
from ..extensions import db,ma

class Car_frames(db.Model):
    __tablename__ = 'car_frame'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    cars=db.relationship("Cars",backref="car_frame",lazy=True,cascade="all, delete-orphan")
    frameComponents=db.relationship("Frame_Components",backref="car_frame",lazy=True,cascade="all, delete-orphan")
    
    def __init__(self,name):
        self.name=name

class CarFrame_Schema(ma.Schema):
    class Meta:
        fields=('id','name')

carFrame_schema=CarFrame_Schema()
carFrames_schema=CarFrame_Schema(many=True)
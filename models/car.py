from ..extensions import db,ma

class Cars(db.Model):
    __tablename__ = 'cars'
    id=db.Column(db.Integer,primary_key=True)
    model=db.Column(db.String(100))
    year=db.Column(db.Integer)
    color=db.Column(db.String(100))
    brand=db.Column(db.String(100))
    frame_id=db.Column(db.Integer,db.ForeignKey('car_frame.id'))
    car_number=db.Column(db.String(100),unique=True)

    def __init__(self,model,year,color,brand,frame_id,car_number):
        self.model=model
        self.year=year
        self.color=color
        self.brand=brand
        self.frame_id=frame_id
        self.car_number=car_number
  

class CarSchema(ma.Schema):
    class Meta:
        fields=('id','model','year','color','brand','frame_id','car_number')

car_schema=CarSchema()
cars_schema=CarSchema(many=True)
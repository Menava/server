from server import db,ma
from ..extensions import db,ma

class ServicePlaces(db.Model):
    __tablename__ = 'serviceplace'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True)
    customerCar_id=db.Column(db.Integer,db.ForeignKey('customer_car.id'),nullable=True)
    initChecklist_id=db.Column(db.Integer,db.ForeignKey('init_checklist.id'),nullable=True)
    state=db.Column(db.Float())
    status=db.Column(db.String(100))

    customer_cars=db.relationship('Customers_cars',backref=db.backref('serviceplace', cascade="all, delete-orphan"))

    def __init__(self,name,customerCar_id,initChecklist_id,state,status):
        self.name=name
        self.customerCar_id=customerCar_id
        self.initChecklist_id=initChecklist_id
        self.state=state
        self.status=status

class ServicePlace_Schema(ma.Schema):
    class Meta:
        fields=('id','name','customerCar_id','initChecklist_id','state','status')

servicePlace_schema=ServicePlace_Schema()
servicePlaces_schema=ServicePlace_Schema(many=True)
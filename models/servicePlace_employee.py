from server import db,ma
from ..extensions import db,ma

class ServicePlaces_employees(db.Model):
    __tablename__ = 'serviceplace_employee'
    id=db.Column(db.Integer,primary_key=True)
    servicePlace_id=db.Column(db.Integer,db.ForeignKey('serviceplace.id'))
    employee_id=db.Column(db.Integer,db.ForeignKey('employees.id'))
    role=db.Column(db.String(20))

    service_places=db.relationship('ServicePlaces',backref='serviceplace_employee')
    
    def __init__(self,servicePlace_id,employee_id,role):
        self.servicePlace_id=servicePlace_id
        self.employee_id=employee_id
        self.role=role
    

class ServicePlaceEmployee_schema(ma.Schema):
    class Meta:
        fields=('id','servicePlace_id','employee_id','role')

serviceplaceEmployee_schema=ServicePlaceEmployee_schema()
serviceplaceEmployees_schema=ServicePlaceEmployee_schema(many=True)
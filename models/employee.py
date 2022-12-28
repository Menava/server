from server import db,ma
from ..extensions import db,ma

class Employees(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    position=db.Column(db.String(100))
    username=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    hidden=db.Column(db.Boolean,default=False)

    def __init__(self,name,position,username,password):
        self.name=name
        self.position=position
        self.username=username
        self.password=password

class EmployeeSchema(ma.Schema):
    class Meta:
        fields=('id','name','position','username','password','hidden')

employee_schema=EmployeeSchema()
employees_schema=EmployeeSchema(many=True)
from server import db,ma
from ..extensions import db,ma

class Services(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    service_type=db.Column(db.String(100))
    service_imageName=db.Column(db.String(100))
    service_imagePath=db.Column(db.String(100))
    service_price=db.Column(db.Float)
    service_detail=db.Column(db.String(100))
    hidden=db.Column(db.Boolean,default=False)

    def __init__(self,service_type,service_imageName,service_imagePath,service_price,service_detail):
        self.service_type=service_type
        self.service_imageName=service_imageName
        self.service_imagePath=service_imagePath
        self.service_price=service_price
        self.service_detail=service_detail

class ServiceSchema(ma.Schema):
    class Meta:
        fields=('id','service_type','service_imageName','service_imagePath','service_price','service_detail','hidden')

service_schema=ServiceSchema()
services_schema=ServiceSchema(many=True)
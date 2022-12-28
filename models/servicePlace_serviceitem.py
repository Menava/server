from server import db,ma
from ..extensions import db,ma

class ServicePlaces_servicesitems(db.Model):
    __tablename__ = 'serviceplace_serviceitem'
    id=db.Column(db.Integer,primary_key=True)
    servicePlace_id=db.Column(db.Integer,db.ForeignKey('serviceplace.id'))
    serviceItem_id=db.Column(db.Integer,db.ForeignKey('serviceitems.id'))
    service_status=db.Column(db.String(100))
    service_places=db.relationship('ServicePlaces',backref='serviceplace_serviceitem')

    def __init__(self,servicePlace_id,serviceItem_id,service_status):
        self.servicePlace_id=servicePlace_id
        self.serviceItem_id=serviceItem_id
        self.service_status=service_status

class ServicePlaceServiceItem_schema(ma.Schema):
    class Meta:
        fields=('id','servicePlace_id','serviceItem_id','service_status')

serviceplaceServiceItem_schema=ServicePlaceServiceItem_schema()
serviceplaceServiceItems_schema=ServicePlaceServiceItem_schema(many=True)
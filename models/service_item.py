from server import db,ma
from ..extensions import db,ma

class Services_items(db.Model):
    __tablename__ = 'serviceitems'
    id=db.Column(db.Integer,primary_key=True)
    service_id=db.Column(db.Integer,db.ForeignKey('services.id'))
    item_id=db.Column(db.Integer,db.ForeignKey('items.id'),nullable=True)
    customerItem_id=db.Column(db.Integer,db.ForeignKey('customer_items.id'),nullable=True)
    service_price=db.Column(db.Float)
    item_price=db.Column(db.Float)
    quantity=db.Column(db.Integer)
    
    services=db.relationship('Services',backref='serviceitems')
    items=db.relationship('Items',backref='serviceitems')
    customer_items=db.relationship('Customer_items',backref='serviceitems')
    
    def __init__(self,service_id,item_id,customerItem_id,service_price,item_price,quantity):
        self.service_id=service_id
        self.item_id=item_id
        self.customerItem_id=customerItem_id
        self.service_price=service_price
        self.item_price=item_price
        self.quantity=quantity


class ServiceItemSchema(ma.Schema):
    class Meta:
        fields=('id','service_id','item_id','customerItem_id','service_price','item_price','quantity')

serviceItem_schema=ServiceItemSchema()
serviceItems_schema=ServiceItemSchema(many=True)
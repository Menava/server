from server import db,ma
from ..extensions import db,ma

class Customer_items(db.Model):
    __tablename__ = 'customer_items'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    customer_id=db.Column(db.Integer,db.ForeignKey('customers.id'))

    customers=db.relationship('Customers',backref=db.backref('customer_items', cascade="all, delete-orphan"))

    def __init__(self,name,customer_id):
        self.name=name
        self.customer_id=customer_id

class CustomerItem_Schema(ma.Schema):
    class Meta:
        fields=('id','name','customer_id')

customerItem_schema=CustomerItem_Schema()
customerItems_schema=CustomerItem_Schema(many=True)
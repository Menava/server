from server import db,ma
from ..extensions import db,ma

class Suppliers(db.Model):
    __tablename__ = 'suppliers'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    hidden=db.Column(db.Boolean,default=False)
    items=db.relationship("Items",backref="suppliers",lazy=True,cascade="all, delete-orphan")

    def __init__(self,name):
        self.name=name

class SupplierSchema(ma.Schema):
    class Meta:
        fields=('id','name','hidden')

supplier_schema=SupplierSchema()
suppliers_schema=SupplierSchema(many=True)
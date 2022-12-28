from server import db,ma
from ..extensions import db,ma

class Items(db.Model):
    __tablename__ = 'items'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    quantity=db.Column(db.Integer)
    price=db.Column(db.Float)
    item_imageName=db.Column(db.String(100))
    item_imagePath=db.Column(db.String(100))
    refundable=db.Column(db.Boolean)
    hidden=db.Column(db.Boolean,default=False)

    supplier_id=db.Column(db.Integer,db.ForeignKey('suppliers.id'))

    def __init__(self,name,quantity,price,item_imageName,item_imagePath,refundable,supplier_id):
        self.name=name
        self.quantity=quantity
        self.price=price
        self.item_imageName=item_imageName
        self.item_imagePath=item_imagePath
        self.refundable=refundable
        self.supplier_id=supplier_id

class ItemSchema(ma.Schema):
    class Meta:
        fields=('id','name','quantity','price','item_imageName','item_imagePath','refundable','refundable','supplier_id')

item_schema=ItemSchema()
items_schema=ItemSchema(many=True)
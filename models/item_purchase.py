from server import db,ma
from ..extensions import db,ma,d_truncated

class Items_Purchase(db.Model):
    __tablename__ = 'item_purchase'
    id=db.Column(db.Integer,primary_key=True)
    purchase_date=db.Column(db.Date,default=d_truncated)
    quantity_received=db.Column(db.Integer)
    refund_quantity=db.Column(db.Integer)
    unit_price=db.Column(db.Float)
    status=db.Column(db.Boolean)

    item_id=db.Column(db.Integer,db.ForeignKey('items.id'))

    def __init__(self,quantity_received,refund_quantity,unit_price,item_id,status):
        self.quantity_received=quantity_received
        self.refund_quantity=refund_quantity
        self.unit_price=unit_price
        self.item_id=item_id
        self.status=status

class ItemPurchase_schema(ma.Schema):
    class Meta:
        fields=('id','purchase_date','quantity_received','refund_quantity','unit_price','item_id','status')

itemPurchase_schema=ItemPurchase_schema()
itemPurchases_schema=ItemPurchase_schema(many=True)
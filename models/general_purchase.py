from server import db,ma
from ..extensions import db,ma,d_truncated

class General_Purchases(db.Model):
    __tablename__ = 'general_purchase'
    id=db.Column(db.Integer,primary_key=True)
    description=db.Column(db.String(150))
    unit_price=db.Column(db.Float)
    quantity=db.Column(db.Integer)
    purchase_type=db.Column(db.String(20))
    total=db.Column(db.Float)
    purchase_date=db.Column(db.Date,default=d_truncated)

    def __init__(self,description,unit_price,quantity,purchase_type,total):
        self.description=description
        self.unit_price=unit_price
        self.quantity=quantity
        self.purchase_type=purchase_type
        self.total=total

class GeneralPurchase_schema(ma.Schema):
    class Meta:
        fields=('id','description','unit_price','quantity','purchase_type','total','purchase_date')

generalPurchase_schema=GeneralPurchase_schema()
generalPurchases_schema=GeneralPurchase_schema(many=True)
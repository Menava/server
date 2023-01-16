from server import db,ma
from ..extensions import db,ma,getTodayDate

class Items_Payment(db.Model):
    __tablename__ = 'item_payment'
    id=db.Column(db.Integer,primary_key=True)
    payment_date=db.Column(db.Date,default=getTodayDate())
    paid_amount=db.Column(db.Float)

    purchase_id=db.Column(db.Integer,db.ForeignKey('item_purchase.id'))

    def __init__(self,paid_amount,purchase_id):
        self.paid_amount=paid_amount
        self.purchase_id=purchase_id

class ItemPayment_schema(ma.Schema):
    class Meta:
        fields=('id','payment_date','paid_amount','purchase_id')


itemPayment_schema=ItemPayment_schema()
itemPayments_schema=ItemPayment_schema(many=True)
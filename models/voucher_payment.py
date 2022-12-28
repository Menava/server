from server import db,ma
from ..extensions import db,ma,d_truncated

class Vouchers_Payment(db.Model):
    __tablename__ = 'voucher_payment'
    id=db.Column(db.Integer,primary_key=True)
    payment_date=db.Column(db.Date,default=d_truncated)
    total_amount=db.Column(db.Float)
    paid_amount=db.Column(db.Float)
    due_date=db.Column(db.Date,default=d_truncated)

    voucher_id=db.Column(db.Integer,db.ForeignKey('vouchers.id'))

    def __init__(self,total_amount,paid_amount,due_date,voucher_id):
        self.total_amount=total_amount
        self.paid_amount=paid_amount
        self.due_date=due_date
        self.voucher_id=voucher_id

class VoucherPayment_schema(ma.Schema):
    class Meta:
        fields=('id','payment_date','total_amount','paid_amount','due_date','voucher_id')

voucherPayment_schema=VoucherPayment_schema()
voucherPayments_schema=VoucherPayment_schema(many=True)
from server import db,ma
from ..extensions import db,ma

class Vouchers_outsources(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    voucher_id=db.Column(db.Integer,db.ForeignKey('vouchers.id'))
    item_name=db.Column(db.String(50))
    source_name=db.Column(db.String(30))
    quantity=db.Column(db.Integer)
    price=db.Column(db.Float)
    total=db.Column(db.Float)
    status=db.Column(db.Boolean,default=False)
    vouchers=db.relationship('Vouchers',backref='vouchers_outsources')
    
    def __init__(self,voucher_id,item_name,source_name,quantity,price,total,status=False):
        self.voucher_id=voucher_id
        self.item_name=item_name
        self.source_name=source_name
        self.quantity=quantity
        self.price=price
        self.total=total
        self.status=status

class VoucherOutsource_schema(ma.Schema):
    class Meta:
        fields=('id','voucher_id','item_name','source_name','quantity','price','total','status')

voucheroutsource_schema=VoucherOutsource_schema()
voucheroutsources_schema=VoucherOutsource_schema(many=True)
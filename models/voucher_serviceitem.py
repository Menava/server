from server import db,ma
from ..extensions import db,ma

class Vouchers_servicesitems(db.Model):
    __tablename__ = 'voucher_serviceitem'
    id=db.Column(db.Integer,primary_key=True)
    service_place=db.Column(db.String(100))
    voucher_id=db.Column(db.Integer,db.ForeignKey('vouchers.id'))
    serviceItem_id=db.Column(db.Integer,db.ForeignKey('serviceitems.id'))
    vouchers=db.relationship('Vouchers',backref='vouchers_servicesitems')

    def __init__(self,service_place,voucher_id,serviceItem_id):
        self.service_place=service_place
        self.voucher_id=voucher_id
        self.serviceItem_id=serviceItem_id

class VoucherServiceItem_schema(ma.Schema):
    class Meta:
        fields=('id','service_place','voucher_id','serviceItem_id')

voucherServiceItem_schema=VoucherServiceItem_schema()
voucherServiceItems_schema=VoucherServiceItem_schema(many=True)
from server import db,ma
from ..extensions import db,ma,getTodayDate


class Vouchers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    customerCar_id=db.Column(db.Integer,db.ForeignKey('customer_car.id'),nullable=False)
    initChecklist_id=db.Column(db.Integer,db.ForeignKey('init_checklist.id'))
    finalChecklist_id=db.Column(db.Integer,db.ForeignKey('final_checklist.id'))
    date=db.Column(db.Date,default=getTodayDate())
    total=db.Column(db.Float())

    customer_cars=db.relationship('Customers_cars',backref=db.backref('vouchers', cascade="all, delete-orphan"))


    def __init__(self,customerCar_id,initChecklist_id,finalChecklist_id,total):
        self.customerCar_id=customerCar_id
        self.initChecklist_id=initChecklist_id
        self.finalChecklist_id=finalChecklist_id
        self.total=total
 

class VoucherSchema(ma.Schema):
    class Meta:
        fields=('id','customerCar_id','initChecklist_id','finalChecklist_id','date','total')

voucher_schema=VoucherSchema()
vouchers_schema=VoucherSchema(many=True)
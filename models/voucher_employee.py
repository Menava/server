from server import db,ma
from ..extensions import db,ma

class Vouchers_employees(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    voucher_id=db.Column(db.Integer,db.ForeignKey('vouchers.id'))
    employee_id=db.Column(db.Integer,db.ForeignKey('employees.id'))
    role=db.Column(db.String(20))

    vouchers=db.relationship('Vouchers',backref='vouchers_employees')
    
    def __init__(self,voucher_id,employee_id,role):
        self.voucher_id=voucher_id
        self.employee_id=employee_id
        self.role=role

class VoucherEmployee_schema(ma.Schema):
    class Meta:
        fields=('id','voucher_id','employee_id','role')

voucherEmployee_schema=VoucherEmployee_schema()
voucherEmployees_schema=VoucherEmployee_schema(many=True)
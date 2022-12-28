from server import db,ma
from ..extensions import db,ma

class Initial_Checklists(db.Model):
    __tablename__ = 'init_checklist'
    id=db.Column(db.Integer,primary_key=True)
    employee_sign=db.Column(db.String(100))
    employee_signPath=db.Column(db.String(100))
    customer_sign=db.Column(db.String(100))
    customer_signPath=db.Column(db.String(100))
    notes=db.Column(db.Text)
    init_images=db.relationship('Init_Checklist_Images',backref='init_checklist')
    vouchers=db.relationship('Vouchers',backref='init_checklist')

    def __init__(self,employee_sign,employee_signPath,customer_sign,customer_signPath,notes):
        self.employee_sign=employee_sign
        self.employee_signPath=employee_signPath
        self.customer_sign=customer_sign
        self.customer_signPath=customer_signPath
        self.notes=notes
        

class InitialChecklist_Schema(ma.Schema):
    class Meta:
        fields=('id','employee_sign','employee_signPath','customer_sign','customer_signPath','notes')

initialChecklist_schema=InitialChecklist_Schema()
initialChecklists_schema=InitialChecklist_Schema(many=True)
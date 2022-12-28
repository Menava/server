from server import db,ma
from ..extensions import db,ma

class Final_Checklists(db.Model):
    __tablename__ = 'final_checklist'
    id=db.Column(db.Integer,primary_key=True)
    employee_sign=db.Column(db.String(100))
    employee_signPath=db.Column(db.String(100))
    customer_sign=db.Column(db.String(100))
    customer_signPath=db.Column(db.String(100))
    notes=db.Column(db.Text)
    customer_rating=db.Column(db.Integer)
    final_images=db.relationship('Final_Checklist_Images',backref='final_checklist')
    vouchers=db.relationship('Vouchers',backref='final_checklist')
    

    def __init__(self,employee_sign,employee_signPath,customer_sign,customer_signPath,notes,customer_rating):
        self.employee_sign=employee_sign
        self.employee_signPath=employee_signPath
        self.customer_sign=customer_sign
        self.customer_signPath=customer_signPath
        self.notes=notes
        self.customer_rating=customer_rating

        

class FinalChecklist_Schema(ma.Schema):
    class Meta:
        fields=('id','employee_sign','employee_signPath','customer_sign','customer_signPath','notes','customer_rating')

finalChecklist_schema=FinalChecklist_Schema()
finalChecklists_schema=FinalChecklist_Schema(many=True)
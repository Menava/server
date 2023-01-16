from server import db,ma
from ..extensions import db,ma,getTodayDate

class Employees_Payroll(db.Model):
    __tablename__ = 'employee_payroll'
    id=db.Column(db.Integer,primary_key=True)
    salary_amount=db.Column(db.Float)
    paid_date=db.Column(db.Date,default=getTodayDate())

    employee_id=db.Column(db.Integer,db.ForeignKey('employees.id'))

    def __init__(self,salary_amount,employee_id):
        self.salary_amount=salary_amount
        self.employee_id=employee_id

class EmployeePayroll_schema(ma.Schema):
    class Meta:
        fields=('id','salary_amount','paid_date','employee_id')

employeePayroll_schema=EmployeePayroll_schema()
employeePayrolls_schema=EmployeePayroll_schema(many=True)
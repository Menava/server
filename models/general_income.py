from server import db,ma
from ..extensions import db,ma,getTodayDate

class General_Incomes(db.Model):
    __tablename__ = 'general_purchase'
    id=db.Column(db.Integer,primary_key=True)
    description=db.Column(db.String(150))
    amount=db.Column(db.Float)
    income_type=db.Column(db.String(20))
    income_date=db.Column(db.Date,default=getTodayDate())

    def __init__(self,description,amount,income_type):
        self.description=description
        self.amount=amount
        self.income_type=income_type

class GeneralIncome_schema(ma.Schema):
    class Meta:
        fields=('id','description','amount','income_type','income_date')

generalIncome_schema=GeneralIncome_schema()
generalIncomes_schema=GeneralIncome_schema(many=True)
from ..extensions import db,ma

class Customers(db.Model):
    __tablename__ = 'customers'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    phone=db.Column(db.BigInteger,unique=True)

    notifications=db.relationship("Notifications",backref="notification",lazy=True,cascade="all, delete-orphan")

    def __init__(self,name,phone):
        self.name=name
        self.phone=phone

class CustomerSchema(ma.Schema):
    class Meta:
        fields=('id','name','phone')

customer_schema=CustomerSchema()
customers_schema=CustomerSchema(many=True)
from ..extensions import db,ma

class Customers_cars(db.Model):
    __tablename__ = 'customer_car'
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customers.id',ondelete="CASCADE"))
    car_id=db.Column(db.Integer,db.ForeignKey('cars.id',ondelete="CASCADE"))

    # customer=db.relationship("Customers",backref="customer_association")
    # car=db.relationship("Cars",backref="car_association")

    customer=db.relationship("Customers",backref=db.backref("customer_cars",cascade="all, delete-orphan"))
    car=db.relationship("Cars",backref=db.backref("customer_cars",cascade="all, delete-orphan"))

    def __init__(self,customer_id,car_id):
        self.customer_id=customer_id
        self.car_id=car_id

class CustomerCar_schema(ma.Schema):
    class Meta:
        fields=('id','customer_id','car_id')

customerCar_schema=CustomerCar_schema()
customerCars_schema=CustomerCar_schema(many=True)
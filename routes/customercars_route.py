from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.car import Cars,car_schema,cars_schema
from ..models.customer import Customers,customer_schema,customers_schema
from ..models.customer_car import Customers_cars,customerCar_schema,customerCars_schema

customercar_route=Blueprint('customercar_route',__name__)


@customercar_route.route('/customercar/get',methods=['GET'])
def get_customercars():
	all_customercars=Customers_cars.query.all()
	results=customerCars_schema.dump(all_customercars)
	return jsonify(results)


@customercar_route.route('/customercar/get/<id>/',methods=['GET'])
def post_details(id):
	# customerCar=Customers_cars.query.get(id)
	# return customerCar_schema.jsonify(customerCar)


	customerCars = db.session.query(Customers_cars, Customers,Cars).join(Customers).join(Cars).filter(Customers_cars.id==id).all()
	for customerCar, customer,car in customerCars:
		customer_result=customer_schema.dump(customer)
		car_result=car_schema.dump(car)
	
	customerCar_result=customerCar_schema.dump(customerCars[0].Customers_cars)
	customerCar_result['customer_id']=customer_result
	customerCar_result['car_id']=car_result
	return jsonify(customerCar_result)



# @customercar_route.route('/customercar/add',methods=['POST'])
# def add_customercar():
# 	# customer_id=request.json['customer_id']
# 	# car_id=request.json['car_id']

# 	# customerCar=Customers_cars(customer_id,car_id)
# 	# db.session.add(customerCar)
# 	# db.session.commit()
# 	# return customerCar_schema.jsonify(customerCar)


@customercar_route.route('/customercar/add',methods=['POST'])
def add_customercar():
	customer_id=request.json['customer_id']
	car_id=request.json['car_id']

	customerCar=Customers_cars(customer_id,car_id)
	db.session.add(customerCar)
	db.session.commit()

	return customerCar_schema.jsonify(customerCar)

@customercar_route.route('/customercar/update/<id>/',methods=['PUT'])
def update_customercar(id):
	customerCar=Customers_cars.query.get(id)
	
	customer_id=request.json['customer_id']
	car_id=request.json['car_id']

	customerCar.customer_id=customer_id
	customerCar.car_id=car_id

	db.session.commit()
	return customerCar_schema.jsonify(customerCar)

@customercar_route.route('/customercar/delete/<id>/',methods=['DELETE'])
def delete_customercar(id):
	customerCar=Customers_cars.query.get(id)

	db.session.delete(customerCar)
	db.session.commit()
	print('test')

	return customerCar_schema.jsonify(customerCar)

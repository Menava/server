from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.car import Cars,car_schema,cars_schema
from ..models.car_frame import Car_frames,CarFrame_Schema

car_route=Blueprint('car_route',__name__)


@car_route.route('/car/get',methods=['GET'])
def get_cars():
	all_cars=Cars.query.all()
	results=cars_schema.dump(all_cars)
	return jsonify(results)


@car_route.route('/car/get/<id>/',methods=['GET'])
def post_details(id):
	car=Cars.query.get(id)
	return car_schema.jsonify(car)

@car_route.route('/car/add/',methods=['POST'])
def add_car():
	model=request.json['model']
	year=request.json['year']
	color=request.json['color']
	brand=request.json['brand']
	frame_id=request.json['frame_id']
	car_number=request.json['car_number']

	car = Cars.query.filter(Cars.car_number==car_number).first()

	if(car==None):
		car=Cars(model,year,color,brand,frame_id,car_number)
		db.session.add(car)
		db.session.commit()
		return car_schema.jsonify(car)
	else:
		return car_schema.jsonify(car)

@car_route.route('/car/update/<id>/',methods=['PUT'])
def update_customer(id):
	car=Cars.query.get(id)
	
	model=request.json['model']
	year=request.json['year']
	color=request.json['color']
	brand=request.json['brand']
	frame_id=request.json['frame_id']
	car_number=request.json['car_number']

	car.model=model
	car.year=year
	car.color=color
	car.brand=brand
	car.frame_id=frame_id
	car.car_number=car_number

	db.session.commit()
	return car_schema.jsonify(car)

@car_route.route('/car/delete/<id>/',methods=['DELETE'])
def delete_user(id):
	car=Cars.query.get(id)

	db.session.delete(car)
	db.session.commit()

	return car_schema.jsonify(car)
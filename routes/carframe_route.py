from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.car_frame import Car_frames,carFrame_schema,carFrames_schema

carframe_route=Blueprint('carframe_route',__name__)


@carframe_route.route('/carframe/get',methods=['GET'])
def get_items():
	all_carframes=Car_frames.query.all()
	results=carFrames_schema.dump(all_carframes)
	return jsonify(results)


@carframe_route.route('/carframe/get/<id>/',methods=['GET'])
def post_details(id):
	carframe=Car_frames.query.get(id)
	return carFrame_schema.jsonify(carframe)


@carframe_route.route('/carframe/add/',methods=['POST'])
def add_item():
	name=request.data


	carframe=Car_frames(name)
	db.session.add(carframe)
	db.session.commit()
	return carFrame_schema.jsonify(carframe)


@carframe_route.route('/carframe/update/<id>/',methods=['PUT'])
def update_item(id):
	carframe=Car_frames.query.get(id)
	
	name=request.data

	carframe.name=name

	db.session.commit()
	return carFrame_schema.jsonify(carframe)


@carframe_route.route('/carframe/delete/<id>/',methods=['DELETE'])
def delete_item(id):
	carframe=Car_frames.query.get(id)

	db.session.delete(carframe)
	db.session.commit()

	return carFrame_schema.jsonify(carframe)
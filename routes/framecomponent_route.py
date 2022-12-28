from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.frame_components import Frame_Components,frameComponent_schema,frameComponents_schema

framecomponent_route=Blueprint('framecomponent_route',__name__)


@framecomponent_route.route('/framecomponent/get/all/<frame_id>',methods=['GET'])
def get_items(frame_id):
	framecomponent_array=[]
	# all_framecomponents=Frame_Components.query.filter(Frame_Components.frame_id==frame_id).all()
	all_framecomponents= db.session.query(Frame_Components).filter(Frame_Components.frame_id==frame_id).all()
	results=frameComponents_schema.dump(all_framecomponents)
	for result in results:
		result["name"]=result["component"]
		del result["component"]
		framecomponent_array.append(result)

	return jsonify(framecomponent_array)


@framecomponent_route.route('/framecomponent/get/<id>/',methods=['GET'])
def post_details(id):
	framecomponent=Frame_Components.query.get(id)
	return frameComponent_schema.jsonify(framecomponent)


@framecomponent_route.route('/framecomponent/add/',methods=['POST'])
def add_item():
	frame_id=request.json['frame_id']
	component=request.json['component']


	framecomponent=Frame_Components(frame_id,component)
	db.session.add(framecomponent)
	db.session.commit()
	return frameComponent_schema.jsonify(framecomponent)


@framecomponent_route.route('/framecomponent/update/<id>/',methods=['PUT'])
def update_item(id):
	framecomponent=Frame_Components.query.get(id)
	
	frame_id=request.json['frame_id']
	component=request.json['component']

	framecomponent.frame_id=frame_id
	framecomponent.component=component

	db.session.commit()
	return frameComponent_schema.jsonify(framecomponent)


@framecomponent_route.route('/framecomponent/delete/<id>/',methods=['DELETE'])
def delete_item(id):
	framecomponent=Frame_Components.query.get(id)

	db.session.delete(framecomponent)
	db.session.commit()

	return frameComponent_schema.jsonify(framecomponent)
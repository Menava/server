from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,ma
from ..models.damageType import DamageTypes,damageType_schema,damageTypes_schema

damagetype_route=Blueprint('damagetype_route',__name__)


@damagetype_route.route('/damagetype/get',methods=['GET'])
def get_items():
	damageType_array=[]
	all_damagetypes=DamageTypes.query.all()
	results=damageTypes_schema.dump(all_damagetypes)
	for result in results:
		result["name"]=result["description"]
		del result["description"]
		damageType_array.append(result)
	return jsonify(results)


@damagetype_route.route('/damagetype/get/<id>/',methods=['GET'])
def post_details(id):
	damagetype=DamageTypes.query.get(id)
	return damageType_schema.jsonify(damagetype)


@damagetype_route.route('/damagetype/add/',methods=['POST'])
def add_item():
	code=request.json['code']
	description=request.json['description']

	damagetype=DamageTypes(code,description)
	db.session.add(damagetype)
	db.session.commit()
	return damageType_schema.jsonify(damagetype)


@damagetype_route.route('/damagetype/update/<id>/',methods=['PUT'])
def update_item(id):
	damagetype=DamageTypes.query.get(id)
	
	code=request.json['code']
	description=request.json['description']

	damagetype.code=code
	damagetype.description=description

	db.session.commit()
	return damageType_schema.jsonify(damagetype)


@damagetype_route.route('/damagetype/delete/<id>/',methods=['DELETE'])
def delete_item(id):
	damagetype=DamageTypes.query.get(id)

	db.session.delete(damagetype)
	db.session.commit()

	return damageType_schema.jsonify(damagetype)
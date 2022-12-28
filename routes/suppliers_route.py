from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.supplier import Suppliers,supplier_schema,suppliers_schema

supplier_route=Blueprint('supplier_route',__name__)


@supplier_route.route('/supplier/get',methods=['GET'])
def get_suppliers():
	all_suppliers=Suppliers.query.all()
	results=suppliers_schema.dump(all_suppliers)
	return jsonify(results)


@supplier_route.route('/supplier/get/<id>/',methods=['GET'])
def post_details(id):
	supplier=Suppliers.query.get(id)
	return supplier_schema.jsonify(supplier)



@supplier_route.route('/supplier/add',methods=['POST'])
def add_supplier():
	name = request.data

	supplier=Suppliers(name)
	db.session.add(supplier)
	db.session.commit()
	return supplier_schema.jsonify(supplier)


@supplier_route.route('/supplier/update/<id>/',methods=['PUT'])
def update_supplier(id):
	supplier=Suppliers.query.get(id)
	
	name = request.data

	supplier.name=name

	db.session.commit()
	return supplier_schema.jsonify(supplier)

@supplier_route.route('/supplier/delete/<id>/',methods=['PUT'])
def delete_supplier(id):
	supplier=Suppliers.query.get(id)

	supplier.hidden=True
	db.session.commit()

	return supplier_schema.jsonify(supplier)

 
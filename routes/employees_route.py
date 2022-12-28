from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.employee import Employees,employee_schema,employees_schema

employee_route=Blueprint('employee_route',__name__)


@employee_route.route('/employee/get',methods=['GET'])
def get_employees():
	all_employees=Employees.query.all()
	results=employees_schema.dump(all_employees)
	return jsonify(results)


@employee_route.route('/employee/get/<id>/',methods=['GET'])
def post_details(id):
	employee=Employees.query.get(id)
	return employee_schema.jsonify(employee)



@employee_route.route('/employee/add/',methods=['POST'])
def add_item():
	name=request.json['name']
	position=request.json['position']
	username=request.json['username']
	password=request.json['password']


	employee=Employees(name,position,username,password)
	db.session.add(employee)
	db.session.commit()
	return employee_schema.jsonify(employee)


@employee_route.route('/employee/update/<id>/',methods=['PUT'])
def update_item(id):
	employee=Employees.query.get(id)
	
	name=request.json['name']
	position=request.json['position']
	username=request.json['username']
	password=request.json['password']

	employee.name=name
	employee.position=position
	employee.username=username
	employee.password=password

	db.session.commit()
	return employee_schema.jsonify(employee)

@employee_route.route('/employee/delete/<id>/',methods=['PUT'])
def delete_item(id):
	employee=Employees.query.get(id)

	employee.hidden=True
	db.session.commit()

	return employee_schema.jsonify(employee)
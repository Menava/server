from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.service_place import ServicePlaces,servicePlace_schema,servicePlaces_schema
from ..models.servicePlace_employee import ServicePlaces_employees,serviceplaceEmployee_schema,serviceplaceEmployees_schema
from ..models.employee import Employees,employee_schema,employees_schema
from array import *
import json

serviceplaceEmployee_route=Blueprint('serviceplaceEmployee_route',__name__)


@serviceplaceEmployee_route.route('/serviceplaceemployee/get',methods=['GET'])
def get_serviceplaceemployees():
	serviceplaceEmployee_array=[]

	serviceplace_employees = db.session.query(ServicePlaces_employees, Employees).join(Employees).all()
	for serviceplace_employee, employee in serviceplace_employees:
		result=serviceplaceEmployee_schema.dump(serviceplace_employee)
		employee_result=employee_schema.dump(employee)
		result["employee_id"]=employee_result
		serviceplaceEmployee_array.append(result)
	return jsonify(serviceplaceEmployee_array)


@serviceplaceEmployee_route.route('/serviceplaceemployee/get/<servicePlace_id>/',methods=['GET'])
def post_details(servicePlace_id):
	serviceplaceEmployee_array=[]

	serviceplace_employees = db.session.query(ServicePlaces_employees, Employees).filter(ServicePlaces_employees.servicePlace_id==servicePlace_id).join(Employees).all()
	for serviceplace_employee, employee in serviceplace_employees:
		result=serviceplaceEmployee_schema.dump(serviceplace_employee)
		employee_result=employee_schema.dump(employee)
		result["employee_id"]=employee_result
		serviceplaceEmployee_array.append(result)
	return jsonify(serviceplaceEmployee_array)


@serviceplaceEmployee_route.route('/serviceplaceemployee/add/',methods=['POST'])
def add_serviceplaceemployee():
	array_data= request.form['array']
	employee_leader_id=request.form.get('employee_leader_id')
	serviceplace_id=request.form.get('serviceplace_id')
	modified_array=json.loads(array_data)
	
	employee_leader=Employees.query.filter(Employees.id==employee_leader_id).first()
	employee_leader_result=employee_schema.dump(employee_leader)
	employee_leader_result["position"]="leader"

	modified_array.append(employee_leader_result)

	for employee in modified_array:
		serviceplace_employee=ServicePlaces_employees(serviceplace_id,employee["id"],employee["position"])
		db.session.add(serviceplace_employee)
	
	db.session.commit()


	return serviceplaceEmployee_schema.jsonify(serviceplace_employee)

@serviceplaceEmployee_route.route('/serviceplaceemployee/update/byserviceplaceID/<servicePlace_id>/<new_servicePlace_id>',methods=['PUT'])
def update_serviceplaceemployee_serviceplaceID(servicePlace_id,new_servicePlace_id):
	serviceplace_employee=ServicePlaces_employees.query.get(id)

	serviceplace_employees = db.session.query(ServicePlaces_employees).filter(ServicePlaces_employees.servicePlace_id==servicePlace_id).all()

	for serviceplace_employee in serviceplace_employees:
		serviceplace_employee.servicePlace_id=new_servicePlace_id
		db.session.commit()
	
	return serviceplaceEmployee_schema.jsonify(serviceplace_employees)

@serviceplaceEmployee_route.route('/serviceplaceemployee/update/<id>/',methods=['PUT'])
def update_serviceplaceemployee(id):
	serviceplace_employee=ServicePlaces_employees.query.get(id)
	
	serviceplace_id=request.json['servicePlace_id']
	employee_id=request.json['employee_id']
	role=request.json['role']

	serviceplace_employee.servicePlace_id=servicePlace_id
	serviceplace_employee.employee_id=employee_id
	serviceplace_employee.role=role

	db.session.commit()
	return serviceplaceEmployee_schema.jsonify(serviceplace_employee)

@serviceplaceEmployee_route.route('/serviceplaceemployee/delete/<id>/',methods=['DELETE'])
def delete_serviceplaceemployee(id):
	voucheremployee=ServicePlaces_employees.query.get(id)

	db.session.delete(voucheremployee)
	db.session.commit()

	return voucherEmployee_schema.jsonify(voucheremployee)

from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.voucher import Vouchers,voucher_schema,vouchers_schema
from ..models.voucher_employee import Vouchers_employees,voucherEmployee_schema,voucherEmployees_schema
from ..models.employee import Employees,employee_schema,employees_schema
from array import *

voucheremployee_route=Blueprint('voucheremployee_route',__name__)


@voucheremployee_route.route('/voucheremployee/get',methods=['GET'])
def get_voucheremployees():
	all_voucheremployees=Vouchers_employees.query.all()
	results=voucherEmployees_schema.dump(all_voucheremployees)
	return jsonify(results)


@voucheremployee_route.route('/voucheremployee/get/<voucher_id>/',methods=['GET'])
def post_details(voucher_id):
	voucherEmployee_array=[]
	# select_voucherEmployees=Vouchers_employees.query.filter(Vouchers_employees.voucher_id==voucher_id)
	# results=voucherEmployees_schema.dump(select_voucherEmployees)
	# return jsonify(results)

	vouchers_employees = db.session.query(Vouchers_employees, Employees).filter(Vouchers_employees.voucher_id==voucher_id).join(Employees).all()
	for vouchers_employee, employee in vouchers_employees:
		voucher_result=voucherEmployee_schema.dump(vouchers_employee)
		employee_result=employee_schema.dump(employee)
		voucher_result["employee_id"]=employee_result
		voucherEmployee_array.append(voucher_result)	
	return jsonify(voucherEmployee_array)


@voucheremployee_route.route('/voucheremployee/add/',methods=['POST'])
def add_voucheremployee():
	voucher_id=request.json['voucher_id']
	employee_id=request.json['employee_id']
	role=request.json['role']

	voucheremployee=Vouchers_employees(voucher_id,employee_id,role)
	db.session.add(voucheremployee)
	db.session.commit()
	return voucherEmployee_schema.jsonify(voucheremployee)


@voucheremployee_route.route('/voucheremployee/update/<id>/',methods=['PUT'])
def update_voucheremployee(id):
	voucheremployee=Vouchers_employees.query.get(id)
	
	voucher_id=request.json['voucher_id']
	employee_id=request.json['employee_id']

	voucheremployee.voucher_id=voucher_id
	voucheremployee.employee_id=employee_id

	db.session.commit()
	return voucherEmployee_schema.jsonify(voucheremployee)

@voucheremployee_route.route('/voucheremployee/delete/<id>/',methods=['DELETE'])
def delete_voucheremployee(id):
	voucheremployee=Vouchers_employees.query.get(id)

	db.session.delete(voucheremployee)
	db.session.commit()

	return voucherEmployee_schema.jsonify(voucheremployee)

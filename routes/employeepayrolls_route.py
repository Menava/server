from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,getTodayDate
from ..models.employee import Employees,employee_schema,employees_schema
from ..models.employee_payroll import Employees_Payroll,employeePayroll_schema,employeePayrolls_schema

employeepayrolls_route=Blueprint('employeepayrolls_route',__name__)


@employeepayrolls_route.route('/employee-payroll/get',methods=['GET'])
def get_employeePayrolls():
    result_array=[]
    results=db.session.query(Employees_Payroll,Employees).join(Employees).all()
    for employeepayroll,employee in results:
        employeepayroll_result=employeePayroll_schema.dump(employeepayroll)
        employee_result=employee_schema.dump(employee)
        employeepayroll_result["employee_id"]=employee_result
        result_array.append(employeepayroll_result)

    return jsonify(result_array)

@employeepayrolls_route.route('/employee-payroll/get/<id>/',methods=['GET'])
def get_employeePayroll(id):
    employeepayrolls=db.sesion.query(Employees_Payroll,Employees).get(Employees_Payroll.id)
    for employeepayroll,employee in employeepayrolls:
        return employeePayroll_schema.jsonify(employeepayroll)



@employeepayrolls_route.route('/employee-payroll/add/',methods=['POST'])
def add_employeePayroll():
    salary_amount=request.json['salary_amount']
    employee_id=request.json['employee_id']

    employee_payroll=Employees_Payroll(salary_amount,employee_id)
    db.session.add(employee_payroll)
    db.session.commit()
    return employeePayroll_schema.jsonify(employee_payroll)

@employeepayrolls_route.route('/employee-payroll/update/<id>/',methods=['PUT'])
def update_employeePayroll(id):
    ep=Employees_Payroll.query.get(id)

    salary_amount=request.json['salary_amount']

    ep.salary_amount=salary_amount

    db.session.commit()
    return employeePayroll_schema.jsonify(ep)

@employeepayrolls_route.route('/employee-payroll/delete/<id>/',methods=['DELETE'])
def delete_employeePayroll(id):
    ep=Employees_Payroll.query.get(id)

    db.session.delete(ep)
    db.session.commit()

    return employeePayroll_schema.jsonify(ep)
from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,getTodayDate
from ..models.general_purchase import General_Purchases,generalPurchase_schema,generalPurchases_schema
from ..models.employee_payroll import Employees_Payroll,employeePayroll_schema,employeePayrolls_schema
from datetime import date

generalpurchase_route=Blueprint('generalpurchase_route',__name__)


@generalpurchase_route.route('/generalpurchase/get',methods=['GET'])
def get_generalpurchases():
	all_generalpurchases=General_Purchases.query.all()
	results=generalPurchases_schema.dump(all_generalpurchases)
	return jsonify(results)


@generalpurchase_route.route('/generalpurchase/get/<id>/',methods=['GET'])
def get_generalpurchase(id):
    generalpurchase = General_Purchases.query.get(id)
    return generalPurchase_schema.jsonify(generalpurchase)



@generalpurchase_route.route('/generalpurchase/add/',methods=['POST'])
def add_generalpurchase():
    description=request.json['description']
    unit_price=request.json['unit_price']
    quantity=request.json['quantity']
    purchase_type=request.json['purchase_type']
    business_type=request.json['business_type']

    total=unit_price*quantity

    generalPurchase=General_Purchases(description,unit_price,quantity,purchase_type,business_type,total)
    db.session.add(generalPurchase)
    db.session.commit()
    return generalPurchase_schema.jsonify(generalPurchase)

@generalpurchase_route.route('/generalpurchase/update/<id>/',methods=['PUT'])
def update_generalpurchase(id):
    gp=General_Purchases.query.get(id)

    description=request.json['description']
    unit_price=request.json['unit_price']
    quantity=request.json['quantity']
    purchase_type=request.json['purchase_type']
    business_type=request.json['business_type']

    gp.description=description
    gp.unit_price=unit_price
    gp.quantity=quantity
    gp.total=int(unit_price)*int(quantity)
    gp.purchase_type=purchase_type
    gp.business_type=business_type

    db.session.commit()
    return generalPurchase_schema.jsonify(gp)

@generalpurchase_route.route('/generalpurchase/delete/<id>/',methods=['DELETE'])
def delete_generalpurchase(id):
    gp=General_Purchases.query.get(id)

    db.session.delete(gp)
    db.session.commit()

    return generalPurchase_schema.jsonify(gp)
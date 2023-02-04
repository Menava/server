from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,getTodayDate
from ..models.general_income import General_Incomes,generalIncome_schema,generalIncomes_schema
from datetime import date

generalincome_route=Blueprint('generalincome_route',__name__)


@generalincome_route.route('/generalincome/get',methods=['GET'])
def get_generalIncomes():
	all_generalIncomes=General_Incomes.query.all()
	results=generalIncomes_schema.dump(all_generalIncomes)
	return jsonify(results)


@generalincome_route.route('/generalincome/get/<id>/',methods=['GET'])
def get_generalIncome(id):
    generalIncome = General_Incomes.query.get(id)
    return generalIncome_schema.jsonify(generalIncome)



@generalincome_route.route('/generalincome/add/',methods=['POST'])
def add_generalIncome():
    description=request.json['description']
    amount=request.json['amount']
    income_type=request.json['income_type']

    generalIncome=General_Incomes(description,amount,income_type)
    db.session.add(generalIncome)
    db.session.commit()
    return generalIncome_schema.jsonify(generalIncome)

@generalincome_route.route('/generalincome/update/<id>/',methods=['PUT'])
def update_generalIncome(id):
    gp=General_Incomes.query.get(id)

    description=request.json['description']
    amount=request.json['amount']
    income_type=request.json['income_type']

    gp.description=description
    gp.amount=amount
    gp.income_type=income_type

    db.session.commit()
    return generalIncome_schema.jsonify(gp)

@generalincome_route.route('/generalincome/delete/<id>/',methods=['DELETE'])
def delete_generalIncome(id):
    gp=General_Incomes.query.get(id)

    db.session.delete(gp)
    db.session.commit()

    return generalIncome_schema.jsonify(gp)
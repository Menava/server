from flask import jsonify, request, render_template, redirect, Blueprint
from ..extensions import db
from ..models.customer import Customers,customer_schema,customers_schema

customer_route = Blueprint('customer_route', __name__)

@customer_route.route('/customer/get', methods=['GET'])
def get_customers():
    all_customers = Customers.query.all()
    results = customers_schema.dump(all_customers)
    return jsonify(results)


@customer_route.route('/customer/get/<id>/', methods=['GET'])
def post_details(id):
    customer = Customers.query.get(id)
    return customer_schema.jsonify(customer)


@customer_route.route('/customer/add', methods=['POST'])
def add_customer():
    name = request.json['name']
    phone = request.json['phone']

    customer = Customers.query.filter(Customers.phone==phone).first()
    if(customer==None):
        customer = Customers(name, phone)
        db.session.add(customer)
        db.session.commit()
        return customer_schema.jsonify(customer)
    else:
        return customer_schema.jsonify(customer)


@customer_route.route('/customer/update/<id>/', methods=['PUT'])
def update_customer(id):
    customer = Customers.query.get(id)

    name = request.json['name']
    phone = request.json['phone']

    customer.name = name
    customer.phone = phone

    db.session.commit()
    return customer_schema.jsonify(customer)


@customer_route.route('/customer/delete/<id>/', methods=['DELETE'])
def delete_user(id):
    customer = Customers.query.get(id)

    db.session.delete(customer)
    db.session.commit()

    return jsonify(customer_schema.dump(customer))
from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,d_truncated

from ..models.item import Items,item_schema,items_schema
from ..models.item_payment import Items_Payment,itemPayment_schema,itemPayments_schema
from datetime import date

itempayments_route=Blueprint('itempayments_route',__name__)

@itempayments_route.route('/item_payment/get',methods=['GET'])
def get_itemPayments():
	pass

@itempayments_route.route('/item_payment/get/<id>/',methods=['GET'])
def get_itemPayment(id):
    item_payment=Items_Payment.query.filter(Items_Payment.purchase_id==id).all()
    return itemPayments_schema.jsonify(item_payment)

@itempayments_route.route('/item_payment/add/',methods=['POST'])
def add_itemPayment():
    paid_amount=request.json['paid_amount']
    purchase_id=request.json['purchase_id']

    itemPaymet=Items_Payment(paid_amount,purchase_id)
    db.session.add(itemPaymet)
    db.session.commit()
    
    return itemPayment_schema.jsonify(itemPaymet)

@itempayments_route.route('/item_payment/update/<id>/',methods=['PUT'])
def update_itemPayment(id):
    pass

@itempayments_route.route('/item_payment/delete/<id>/',methods=['DELETE'])
def delete_itemPayment(id):
    pass
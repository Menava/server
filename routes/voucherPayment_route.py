from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,d_truncated

from ..models.voucher import Vouchers,voucher_schema,vouchers_schema
from ..models.voucher_payment import Vouchers_Payment,voucherPayment_schema,voucherPayments_schema
from datetime import date

voucherPayment_route=Blueprint('voucherPayment_route',__name__)

@voucherPayment_route.route('/voucher_payment/get',methods=['GET'])
def get_voucherPayment():
	pass

@voucherPayment_route.route('/voucher_payment/get/<id>/',methods=['GET'])
def post_details(id):
    voucher_payment = Vouchers_Payment.query.get(id)
    return voucherPayment_schema.jsonify(voucher_payment)

@voucherPayment_route.route('/voucher_payment/add/<day>/<month>/<year>/',methods=['POST'])
def add_voucherPayment(day,month,year):
    total_amount=request.json['total_amount']
    paid_amount=request.json['paid_amount']
    voucher_id=request.json['voucher_id']

    due_date=date(year=int(year),month=int(month),day=int(day))

    voucherPaymet=Vouchers_Payment(total_amount,paid_amount,due_date,voucher_id)
    db.session.add(voucherPaymet)
    db.session.commit()
    
    return voucherPayment_schema.jsonify(voucherPaymet)

@voucherPayment_route.route('/voucher_payment/update/<id>/',methods=['PUT'])
def update_voucherPayment(id):
    voucher_payment = Vouchers_Payment.query.get(id)

    paid_amount = request.json['paid_amount']
    print(paid_amount)
    voucher_payment.paid_amount =paid_amount

    db.session.commit()
    return voucherPayment_schema.jsonify(voucher_payment)

@voucherPayment_route.route('/voucher_payment/delete/<id>/',methods=['DELETE'])
def delete_voucherPayment(id):
    pass
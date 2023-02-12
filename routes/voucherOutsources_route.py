from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.voucher import Vouchers,voucher_schema,vouchers_schema
from ..models.voucher_outsource import Vouchers_outsources,voucheroutsource_schema,voucheroutsources_schema

voucherOutsources_route=Blueprint('voucherOutsources_route',__name__)


@voucherOutsources_route.route('/voucheroutsource/get',methods=['GET'])
def get_voucheroutsources():
    vsources=Vouchers_outsources.query.all()
	results=voucheroutsources_schema.dump(vsources)
	return jsonify(results)

@voucherOutsources_route.route('/voucheroutsource/get/<voucher_id>/',methods=['GET'])
def post_details(voucher_id):
    voucher_outsources=Vouchers_outsources.query.filter(Vouchers_outsources.voucher_id==voucher_id).all()

    return voucheroutsources_schema.jsonify(voucher_outsources)

@voucherOutsources_route.route('/voucheroutsource/add/',methods=['POST'])
def add_voucheroutsource():
    voucher_id=request.json['voucher_id']
    item_name=request.json['item_name']
    source_name=request.json['source_name']
    quantity=request.json['quantity']
    price=request.json['price']
    total=request.json['total']

    voucherOutsource=Vouchers_outsources(voucher_id,item_name,source_name,quantity,price,total)
    db.session.add(voucherOutsource)
    
    db.session.commit()

    return voucheroutsource_schema.jsonify(voucherOutsource)

@voucherOutsources_route.route('/voucheroutsource/update/<id>/',methods=['PUT'])
def update_voucheroutsource(id):
    vsource=Vouchers_outsources.query.get(id)

@voucherOutsources_route.route('/voucheroutsource/delete/<id>/',methods=['DELETE'])
def delete_voucheroutsource(id):
    pass

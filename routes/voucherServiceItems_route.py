from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.voucher import Vouchers,voucher_schema,vouchers_schema
from ..models.service_item import Services_items,serviceItem_schema,serviceItems_schema
from ..models.item import Items,item_schema,items_schema
from ..models.customer_item import Customer_items,customerItem_schema,customerItems_schema
from ..models.service import Services,service_schema,services_schema
from ..models.voucher_serviceitem import Vouchers_servicesitems,voucherServiceItem_schema,voucherServiceItems_schema

voucherServiceItem_route=Blueprint('voucherServiceItem_route',__name__)


@voucherServiceItem_route.route('/voucherserviceitem/get',methods=['GET'])
def get_voucherserviceitem():
	all_voucherserviceitems=Vouchers_servicesitems.query.all()
	results=voucherServiceItems_schema.dump(all_voucherserviceitems)
	return jsonify(results)


@voucherServiceItem_route.route('/voucherserviceitem/get/<voucher_id>/',methods=['GET'])
def post_details(voucher_id):
	final_array=[]
	service_line={"service":"","items":[]}

	serviceItem_array=[]
	sorted_array=[]
	service_list={}
	item_list=[]
	pre_serviceid=None
	
	serviceItems=db.session.query(Services_items,Vouchers_servicesitems,Items,Services,Customer_items).filter(Vouchers_servicesitems.voucher_id==voucher_id,Items!=None).outerjoin(Items,Customer_items).join(Vouchers_servicesitems,Services).all()
	for serviceItem,serviceplace_item,item,service,customer_item in serviceItems:
		serviceItem_result=serviceItem_schema.dump(serviceItem)
		if(item!=None):
			item.price=serviceItem_result['item_price']
		serviceItem_result["item_id"]=item
		serviceItem_result["service"]=service
		serviceItem_result["customerItem_id"]=customer_item
		serviceItem_array.append(serviceItem_result)
	serviceItem_array.sort(key=sortBy_serviceID)
	
	# print(serviceItem_array)
	for serviceItem in serviceItem_array:
		print(serviceItem)
		item_result=item_schema.dump(serviceItem["item_id"])
		# print(item_result)
		if(item_result!={}):
			item_result["quantity"]=serviceItem["quantity"]
			item_result["price"]=serviceItem["item_price"]
		customerItem_result=customerItem_schema.dump(serviceItem["customerItem_id"])
		if(customerItem_result!={}):
			customerItem_result["quantity"]=serviceItem["quantity"]
		if(pre_serviceid==None):
			pre_serviceid=serviceItem["service_id"]
		if(serviceItem["service_id"]!=pre_serviceid):
			item_list=[]
		if(serviceItem["item_id"]!=None):
			item_list.append(item_result)
		else:
			item_list.append(customerItem_result)
		
		service_list[serviceItem["service_id"]]=[]
		service_list[serviceItem["service_id"]].append(item_list)
		service_list[serviceItem["service_id"]].append(serviceItem["service_price"])
		pre_serviceid=serviceItem["service_id"]
		# print(service_list)
	# print('service_list',service_list)
	for service,items in service_list.items():
		if(items[0]==[{}]):
			items[0]=[]
		service=Services.query.filter(Services.id==service).first()
		service_result=service_schema.dump(service)
		# print("items[2]--------------------------------------",items)
		service_line["service"]=service_result
		service_line["service"]["service_price"]=items[1]
		service_line["items"]=items[0]
		final_array.append(service_line.copy())
	
	# print('finaly array',final_array)
	return jsonify(final_array)

@voucherServiceItem_route.route('/voucherserviceitem/add/',methods=['POST'])
def add_voucherserviceitem():
	service_place=request.json['service_place']
	voucher_id=request.json['voucher_id']
	serviceItem_id=request.json['serviceItem_id']

	voucherserviceitem=Vouchers_servicesitems(service_place,voucher_id,serviceItem_id)
	db.session.add(voucherserviceitem)
	db.session.commit()
	return voucherServiceItem_schema.jsonify(voucherserviceitem)


@voucherServiceItem_route.route('/voucherserviceitem/update/<id>/',methods=['PUT'])
def update_voucherserviceitem(id):
	voucherserviceitem=Vouchers_servicesitems.query.get(id)
	
	service_place=request.json['service_place']
	voucher_id=request.json['voucher_id']
	serviceItem_id=request.json['serviceItem_id']

	voucherserviceitem.service_place=service_place
	voucherserviceitem.voucher_id=voucher_id
	voucherserviceitem.serviceItem_id=serviceItem_id

	db.session.commit()
	return voucherServiceItem_schema.jsonify(voucherserviceitem)

@voucherServiceItem_route.route('/voucherserviceitem/delete/<id>/',methods=['DELETE'])
def delete_voucherserviceitem(id):
	voucherserviceitem=Vouchers_servicesitems.query.get(id)

	db.session.delete(voucherserviceitem)
	db.session.commit()

	return voucherServiceItem_schema.jsonify(voucherserviceitem)

def sortBy_serviceID(item):
	return item["service_id"]

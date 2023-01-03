from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.service_place import ServicePlaces,servicePlace_schema,servicePlaces_schema
from ..models.service_item import Services_items,serviceItem_schema,serviceItems_schema
from ..models.item import Items,item_schema,items_schema
from ..models.customer_item import Customer_items,customerItem_schema,customerItems_schema
from ..models.service import Services,service_schema,services_schema
from ..models.servicePlace_serviceitem import ServicePlaces_servicesitems,serviceplaceServiceItem_schema,serviceplaceServiceItems_schema
from ..models.voucher_serviceitem import Vouchers_servicesitems,voucherServiceItem_schema,voucherServiceItems_schema
import json

serviceplaceServiceItem_route=Blueprint('serviceplaceServiceItem_route',__name__)


@serviceplaceServiceItem_route.route('/serviceplaceserviceitem/get',methods=['GET'])
def get_voucherserviceitem():
	serviceplaceDetails=[]
	dist={"serviceplace_serviceitem":serviceplaceDetails}

	serviceplace_serviceItems = db.session.query(ServicePlaces_servicesitems, Services_items).join(Services_items).all()
	for serviceplace_serviceItem, service_item in serviceplace_serviceItems:
		serviceItems = db.session.query(Services_items,Items,Services,Customer_items).filter(Services_items.id==serviceplace_serviceItem.serviceItem_id,Items!=None).outerjoin(Items).join(Services).outerjoin(Customer_items).all()
		for serviceItem, item,service,customer_item in serviceItems:
			item_result=item_schema.dump(item)
			service_result=service_schema.dump(service)
			customerItem_result=customerItem_schema.dump(customer_item)
		serviceitem_result=serviceItem_schema.dump(service_item)
		serviceitem_result['item_id']=item_result
		serviceitem_result['service_id']=service_result
		serviceitem_result['customerItem_id']=customerItem_result
		serviceplaceDetail_result=serviceplaceServiceItem_schema.dump(serviceplace_serviceItem)
		serviceplaceDetail_result['serviceItem_id']=serviceitem_result
		serviceplaceDetails.append(serviceplaceDetail_result)
	return jsonify(dist)


@serviceplaceServiceItem_route.route('/serviceplaceserviceitem/get/<servicePlace_id>/',methods=['GET'])
def post_details(servicePlace_id):
	serviceplaceDetails=[]
	dist={"voucher_serviceitem":serviceplaceDetails}

	serviceplace_serviceItems = db.session.query(ServicePlaces_servicesitems, Services_items).filter(ServicePlaces_servicesitems.servicePlace_id==servicePlace_id).join(Services_items).all()
	for serviceplace_serviceItem, service_item in serviceplace_serviceItems:
		serviceItems = db.session.query(Services_items,Items,Services,Customer_items).filter(Services_items.id==serviceplace_serviceItem.serviceItem_id,Items!=None).outerjoin(Items).join(Services).outerjoin(Customer_items).all()
		for serviceItem, item,service,customer_item in serviceItems:
			item_result=item_schema.dump(item)
			service_result=service_schema.dump(service)
			customerItem_result=customerItem_schema.dump(customer_item)
		serviceitem_result=serviceItem_schema.dump(service_item)
		serviceitem_result['item_id']=item_result
		serviceitem_result['service_id']=service_result
		serviceitem_result['customerItem_id']=customerItem_result
		serviceplaceDetail_result=serviceplaceServiceItem_schema.dump(serviceplace_serviceItem)
		serviceplaceDetail_result['serviceItem_id']=serviceitem_result
		serviceplaceDetails.append(serviceplaceDetail_result)
	return jsonify(dist)



@serviceplaceServiceItem_route.route('/serviceplaceserviceitem/add/',methods=['POST'])
def add_voucherserviceitem():
	serviceplace_id=request.form.get('serviceplace_id')
	serviceItem_array=request.form.get('serviceItem_array')
	modified_array=json.loads(serviceItem_array)
	service_status="Working"

	for serviceItem in modified_array:
		print(serviceItem)
		serviceplace_serviceitem=ServicePlaces_servicesitems(serviceplace_id,serviceItem["id"],service_status)
		db.session.add(serviceplace_serviceitem)

	db.session.commit()
	return serviceplaceServiceItem_schema.jsonify(serviceplace_serviceitem)

@serviceplaceServiceItem_route.route('/serviceplaceserviceitem/update/byserviceplaceID/<servicePlace_id>/<new_servicePlace_id>',methods=['PUT'])
def update_voucherserviceitem_serviceplaceID(servicePlace_id,new_servicePlace_id):
	serviceplace_serviceItems = db.session.query(ServicePlaces_servicesitems).filter(ServicePlaces_servicesitems.servicePlace_id==servicePlace_id).all()
	for serviceplace_serviceItem in serviceplace_serviceItems:
		serviceplace_serviceItem.servicePlace_id=new_servicePlace_id
		db.session.commit()

	return serviceplaceServiceItem_schema.jsonify(serviceplace_serviceItems)

@serviceplaceServiceItem_route.route('/serviceplaceserviceitem/update/',methods=['PUT'])
def update_voucherserviceitem():
	servicePlace_id=request.json['servicePlace_id']
	service_id=request.json['service_id']
	service_status=request.json['service_status']

	serviceplace_serviceItems = db.session.query(ServicePlaces_servicesitems, Services_items).filter(Services_items.service_id==service_id).join(Services_items).all()
	for serviceplace_item,service_item in serviceplace_serviceItems:
		serviceplaceItem_result=serviceplaceServiceItem_schema.dump(serviceplace_item)
		serviceplaceItem_result["service_status"]=service_status
		
		serviceplace_item.servicePlace_id=serviceplaceItem_result["servicePlace_id"]
		serviceplace_item.serviceItem_id=serviceplaceItem_result["serviceItem_id"]
		serviceplace_item.service_status=serviceplaceItem_result["service_status"]

		db.session.commit()

	refresh_status(servicePlace_id)
	return serviceplaceServiceItem_schema.jsonify(serviceplaceItem_result)

@serviceplaceServiceItem_route.route('/serviceplaceserviceitem/append',methods=['PUT'])
def append_voucherserviceitem():
	print("---------------------------------------------------------")
	servicePlace_id=request.json['servicePlace_id']
	service_id=request.json['service_id']
	item_id=request.json['item_id']
	item_price=request.json['item_price']
	customer_id=request.json['customer_id']
	item_name=request.json['item_name']
	
	print("item_id",item_id)
	print("customer_id",customer_id)

	status_check=False
	customerItem_id=None
	service_price=None
	quantity=1
	service_status="Working"

	if(item_id=="None"):
		item_id=None
		
	serviceplace_serviceItems = db.session.query(ServicePlaces_servicesitems, Services_items).filter(Services_items.service_id==service_id,ServicePlaces_servicesitems.servicePlace_id==servicePlace_id).join(Services_items).all()
	if(serviceplace_serviceItems==[]):
		print("in")
		quantity=0
		serviceItem=Services_items(service_id,item_id,customerItem_id,service_price,item_price,quantity)
		serviceplaceItem_result=serviceplaceServiceItem_schema.dump(serviceItem)
		db.session.add(serviceItem)
		serviceItem_query=Services_items.query.order_by(Services_items.id.desc()).first()
		servicePlace=ServicePlaces_servicesitems(servicePlace_id,serviceItem_query.id,service_status)
		db.session.add(servicePlace)
		db.session.commit()
	else:
		for serviceplace_item,service_item in serviceplace_serviceItems:
			serviceplaceItem_result=serviceplaceServiceItem_schema.dump(serviceplace_item)
			service_item_result=serviceItem_schema.dump(service_item)
			print(service_item_result)
			if(service_item_result["item_id"]==None and service_item_result["customerItem_id"]==None):
				if(item_id==None):
					customerItem=Customer_items(item_name,customer_id)
					db.session.add(customerItem)
					customerItem_query=Customer_items.query.order_by(Customer_items.id.desc()).first()
					service_item.customerItem_id=customerItem_query.id
					service_item.item_price=0
				if(item_id!=None):
					service_item.item_id=item_id
					service_item.item_price=item_price
					update_itemQTY(item_id,quantity)
				service_item.quantity=quantity
				status_check=True
				db.session.commit()

		if(status_check==False):
			if(item_id==None):
				customerItem=Customer_items(item_name,customer_id)
				db.session.add(customerItem)
				customerItem_query=Customer_items.query.order_by(Customer_items.id.desc()).first()
				customerItem_id=customerItem_query.id
			serviceItem=Services_items(service_id,item_id,customerItem_id,service_price,item_price,quantity)
			db.session.add(serviceItem)
			if(item_id!=None):
				update_itemQTY(item_id,quantity)
			serviceItem_query=Services_items.query.order_by(Services_items.id.desc()).first()
			servicePlace=ServicePlaces_servicesitems(servicePlace_id,serviceItem_query.id,service_status)
			db.session.add(servicePlace)
			db.session.commit()
		
	refresh_status(servicePlace_id)
	return serviceplaceServiceItem_schema.jsonify(serviceplaceItem_result)



@serviceplaceServiceItem_route.route('/serviceplaceserviceitem/delete/<id>/',methods=['DELETE'])
def delete_voucherserviceitem(id):
	print("innnnn")
	service_id=request.json['service_id']
	print('service_id',service_id)
	item_id=request.json['item_id']
	print('item_id',item_id)
	customerItem_id=request.json['customerItem_id']

	
	
	print('customerItem_id',customerItem_id)

	if(item_id!="None"):
		print("item in")
		serviceplace_serviceItems = db.session.query(ServicePlaces_servicesitems, Services_items).filter(ServicePlaces_servicesitems.servicePlace_id==id).filter(Services_items.service_id==service_id).filter(Services_items.item_id==item_id).join(Services_items).all()
	if(customerItem_id!="None"):
		print("customer in")
		customerItem = Customer_items.query.get(customerItem_id)
		db.session.delete(customerItem)
		serviceplace_serviceItems = db.session.query(ServicePlaces_servicesitems, Services_items).filter(ServicePlaces_servicesitems.servicePlace_id==id).filter(Services_items.service_id==service_id).filter(Services_items.customerItem_id==customerItem_id).join(Services_items).all()
	if(item_id=="None" and customerItem_id=="None" ):
		print("service in")
		serviceplace_serviceItems = db.session.query(ServicePlaces_servicesitems, Services_items).filter(ServicePlaces_servicesitems.servicePlace_id==id).filter(Services_items.service_id==service_id).join(Services_items).all()
	
	
	for serviceplace_item,service_item in serviceplace_serviceItems:
		serviceItem_result=serviceItem_schema.dump(service_item)
		print(serviceItem_result)
		if(serviceItem_result["item_id"]!=None):
			item=Items.query.get(serviceItem_result["item_id"])
			item.quantity+=serviceItem_result["quantity"]
		
		db.session.delete(serviceplace_item)
		db.session.delete(service_item)
		
	db.session.commit()

	return jsonify("TEST")

@serviceplaceServiceItem_route.route('/serviceplaceserviceitem/edit/<id>/',methods=['PUT'])
def edit_itemQuantity(id):
	service_id=request.json['service_id']
	customerItem_id=request.json['customerItem_id']
	method=request.json['method']
	item_id=request.json['item_id']
	
	if(item_id!="None"):
		serviceplace_serviceItems = db.session.query(ServicePlaces_servicesitems, Services_items).filter(ServicePlaces_servicesitems.servicePlace_id==id).filter(Services_items.service_id==service_id).filter(Services_items.item_id==item_id).join(Services_items).all()
	if(customerItem_id!="None"):
		serviceplace_serviceItems = db.session.query(ServicePlaces_servicesitems, Services_items).filter(ServicePlaces_servicesitems.servicePlace_id==id).filter(Services_items.service_id==service_id).filter(Services_items.customerItem_id==customerItem_id).join(Services_items).all()
	
	for serviceplace_item,service_item in serviceplace_serviceItems:
		serviceItem_result=serviceItem_schema.dump(service_item)
		print(serviceItem_result)
		item=Items.query.get(serviceItem_result["item_id"])	
		if(method=="Plus"):
			if(serviceItem_result["item_id"]!=None):
				if(item.quantity>0):
					service_item.quantity+=1
					item.quantity-=1
			else:
				service_item.quantity+=1
		if(method=="Minus"):
			if(service_item.quantity>0):
				print("minus in")
				service_item.quantity-=1
				if(serviceItem_result["item_id"]!=None):
					item.quantity+=1
			if(service_item.quantity==0):
				print("delete in ")
				db.session.delete(serviceplace_item)
				db.session.delete(service_item)
	db.session.commit()
	
	return jsonify("TEST")

def refresh_status(servicePlace_id=None):
	done_count=0
	return_value=test_method(servicePlace_id)
	serviceplace_items = return_value.get_json()
	
	for serviceplace_item in serviceplace_items:
		if(serviceplace_item["status"]=="Done"):
			done_count+=1
	status_percentage=((done_count/len(serviceplace_items)*100))


	serviceplace=ServicePlaces.query.get(servicePlace_id)
	serviceplace.state=status_percentage

	if(serviceplace.state>=100):
		serviceplace.status="Finished"
	elif (serviceplace.state>=50):
		serviceplace.status="Almost There"
	elif (serviceplace.state>=50):
		serviceplace.status="Half Done"
	elif (serviceplace.state>=0):
		serviceplace.status="On Progress"
	else:
		serviceplace.status="Finished"

	db.session.add(serviceplace)
	db.session.commit()


@serviceplaceServiceItem_route.route('/serviceplaceserviceitem/test/<servicePlace_id>/',methods=['GET'])
def test_method(servicePlace_id):
	final_array=[]
	service_line={"service":"","items":[],"status":""}

	serviceItem_array=[]
	sorted_array=[]
	service_list={}
	item_list=[]
	pre_serviceid=None
	
	serviceItems=db.session.query(Services_items,ServicePlaces_servicesitems,Items,Services,Customer_items).filter(ServicePlaces_servicesitems.servicePlace_id==servicePlace_id,Items!=None).outerjoin(Items,Customer_items).join(ServicePlaces_servicesitems,Services).order_by(Services_items.service_id).all()
	for serviceItem,serviceplace_item,item,service,customer_item in serviceItems:
		serviceItem_result=serviceItem_schema.dump(serviceItem)
		serviceItem_result["service"]=service
		serviceItem_result["serviceplace"]=serviceplace_item.service_status

		item_result=item_schema.dump(item)
		if(item_result!={}):
			item_result["quantity"]=serviceItem_result["quantity"]
			item_result["price"]=serviceItem_result["item_price"]
		customerItem_result=customerItem_schema.dump(customer_item)
		if(customerItem_result!={}):
			customerItem_result["quantity"]=serviceItem_result["quantity"]
		if(pre_serviceid==None):
			pre_serviceid=serviceItem_result["service_id"]
		if(serviceItem_result["service_id"]!=pre_serviceid):
			item_list=[]
		if(serviceItem_result["item_id"]!=None):
			item_list.append(item_result)
		else:
			item_list.append(customerItem_result)

		service_list[serviceItem_result["service_id"]]=[]
		service_list[serviceItem_result["service_id"]].append(item_list)
		service_list[serviceItem_result["service_id"]].append(serviceItem_result["serviceplace"])
		service_list[serviceItem_result["service_id"]].append(serviceItem_result["service_price"])
		pre_serviceid=serviceItem_result["service_id"]

	for service,items in service_list.items():
		if(items[0]==[{}]):
			items[0]=[]
		service=Services.query.filter(Services.id==service).first()
		service_result=service_schema.dump(service)
		service_line["service"]=service_result
		service_line["service"]["service_price"]=items[2]
		service_line["items"]=items[0]
		service_line["status"]=items[1]
		final_array.append(service_line.copy())
	
	return jsonify(final_array)

def update_itemQTY(item_id,quantity):
	item=Items.query.get(item_id)
	
	item.quantity-=quantity

	db.session.add(item)
	db.session.commit()

def loop_serviceItem(voucher_id):
	final_array=[]
	service_line={"service":"","items":[]}

	serviceItem_array=[]
	sorted_array=[]
	service_list={}
	item_list=[]
	pre_serviceid=None
	
	serviceItems=db.session.query(Services_items,Vouchers_servicesitems,Items,Services,Customer_items).filter(Vouchers_servicesitems.voucher_id==voucher_id,Items!=None).outerjoin(Items,Customer_items).join(Vouchers_servicesitems,Services).order_by(Services_items.service_id).all()
	for serviceItem,serviceplace_item,item,service,customer_item in serviceItems:
		serviceItem_result=serviceItem_schema.dump(serviceItem)
		serviceItem_result["service"]=service

		item_result=item_schema.dump(item)
		if(item_result!={}):
			item_result["quantity"]=serviceItem_result["quantity"]
			item_result["price"]=serviceItem_result["item_price"]
		customerItem_result=customerItem_schema.dump(customer_item)
		if(customerItem_result!={}):
			customerItem_result["quantity"]=serviceItem_result["quantity"]
		if(pre_serviceid==None):
			pre_serviceid=serviceItem_result["service_id"]
		if(serviceItem_result["service_id"]!=pre_serviceid):
			item_list=[]
		if(serviceItem_result["item_id"]!=None):
			item_list.append(item_result)
		else:
			pass
		
		service_list[serviceItem_result["service_id"]]=[]
		service_list[serviceItem_result["service_id"]].append(item_list)
		service_list[serviceItem_result["service_id"]].append(serviceItem_result["service_price"])
		pre_serviceid=serviceItem_result["service_id"]

	# print("servicelist",service_list)
	for service,items in service_list.items():
		if(items[0]==[{}]):
			items[0]=[]
		service=Services.query.filter(Services.id==service).first()
		service_result=service_schema.dump(service)
		service_line["service"]=service_result
		service_line["service"]["service_price"]=items[1]
		service_line["items"]=items[0]
		final_array.append(service_line.copy())

	# print(final_array)
	return final_array
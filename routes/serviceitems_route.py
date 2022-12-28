from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.item import Items,item_schema,items_schema
from ..models.service import Services,service_schema,services_schema
from ..models.servicePlace_serviceitem import ServicePlaces_servicesitems,serviceplaceServiceItem_schema,serviceplaceServiceItems_schema
from ..models.service_item import Services_items,serviceItem_schema,serviceItems_schema
from ..models.customer_item import Customer_items,customerItem_schema,customerItems_schema
from ..models.customer import Customers,customer_schema,customers_schema
import json

serviceitem_route=Blueprint('serviceitem_route',__name__)


@serviceitem_route.route('/serviceitem/get',methods=['GET'])
def get_serviceitems():
	all_serviceitems=Services_items.query.all()
	results=serviceItems_schema.dump(all_serviceitems)
	return jsonify(results)


@serviceitem_route.route('/serviceitem/get/<id>/',methods=['GET'])
def post_details(id):
	serviceitem=Services_items.query.get(id)
	return serviceItem_schema.jsonify(serviceitem)



@serviceitem_route.route('/serviceitem/add/',methods=['POST'])
def add_serviceitem():
	customeritem_id=None

	array_data= request.form['array']
	modified_array=json.loads(array_data)
	null_customeritem_id=None
	null_item_id=None
	
	serviceitem_array=[]
	for service_item in modified_array:
		if(service_item["items"]==[]):
			item_id=None
			customeritem_id=None
			item_price=None
			item_quantity=None
			service_item["serviceFee"]=0
			serviceitem=Services_items(service_item["id"],item_id,customeritem_id,service_item["serviceFee"],item_price,item_quantity)

		
			db.session.add(serviceitem)
			db.session.commit()

			serviceItem_query=Services_items.query.order_by(Services_items.id.desc()).first()
			query_result=serviceItem_schema.dump(serviceItem_query)
			serviceitem_array.append(query_result)
		for items in service_item["items"]:
			if 'id' in items:
				customeritem_id=None
				item_id=items["id"]
				update_itemQTY(items["id"],items["qty"])
			else:
				item_id=None
				customer=Customers.query.filter_by(phone=items["customerPhone"]).first()
				customer_result=customer_schema.dump(customer)
				customer_item=Customer_items(items["name"],customer_result["id"])

				db.session.add(customer_item)
				db.session.commit()
				
				customeritem=Customer_items.query.order_by(Customer_items.id.desc()).first()
				customeritem_result=customerItem_schema.dump(customeritem)
				customeritem_id=customeritem_result["id"]

			service_item["serviceFee"]=0
			serviceitem=Services_items(service_item["id"],item_id,customeritem_id,service_item["serviceFee"],items["price"],items["qty"])

	
			db.session.add(serviceitem)
			db.session.commit()
			serviceItem_query=Services_items.query.order_by(Services_items.id.desc()).first()
			query_result=serviceItem_schema.dump(serviceItem_query)
			serviceitem_array.append(query_result)
			
	print("serviceitem_array",serviceitem_array)
	return jsonify(serviceitem_array)


@serviceitem_route.route('/serviceitem/update/',methods=['PUT'])
def update_serviceitem():
	array_data= request.form['array']
	servicePlace_id= request.form['servicePlace_id']
	modified_array=json.loads(array_data)
	service_array=[]
	item_array=[]

	for service_item in modified_array:
		service_result=service_schema.dump(service_item["service"])
		service_array.append(service_result)
		for i in service_item["items"]:
			if 'customer_id' in i.keys():
				service_item["items"].remove(i)

	for service in service_array:
		serviceItem_querys=db.session.query(Services_items).filter(ServicePlaces_servicesitems.servicePlace_id==servicePlace_id).filter(Services_items.service_id==service["id"]).join(ServicePlaces_servicesitems).all()
		query_results=serviceItems_schema.dump(serviceItem_querys)
		for query_result in query_results:
			serviceitem=Services_items.query.get(query_result["id"])
			itemPrice=findIndex_serviceItem(serviceitem,modified_array)
			serviceitem.service_price=service["service_price"]
			serviceitem.item_price=itemPrice
			db.session.commit()


	return serviceItem_schema.jsonify(serviceitem)

def findIndex_serviceItem(serviceitem,modified_array):
	for serviceItem in modified_array:
		if(serviceItem["service"]["id"]==serviceitem.service_id):
			for i in serviceItem["items"]:
				if(serviceitem.item_id==i["id"]):
					return(i["price"])

@serviceitem_route.route('/serviceitem/delete/<id>/',methods=['DELETE'])
def delete_serviceitem(id):
	serviceitem=Services_items.query.get(id)

	db.session.delete(serviceitem)
	db.session.commit()

	return serviceItem_schema.jsonify(serviceitem)

def update_itemQTY(item_id,quantity):
	item=Items.query.get(item_id)
	
	item.quantity-=quantity

	db.session.add(item)
	db.session.commit()


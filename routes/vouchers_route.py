from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,d_truncated
from ..models.voucher import Vouchers,voucher_schema,vouchers_schema
from ..models.service import Services,service_schema,services_schema
from ..models.voucher_serviceitem import Vouchers_servicesitems,voucherServiceItem_schema,voucherServiceItems_schema
from ..models.voucher_payment import Vouchers_Payment,voucherPayment_schema,voucherPayments_schema
from ..models.service_item import Services_items,serviceItem_schema,serviceItems_schema
from ..models.item import Items,item_schema,items_schema

from ..models.customer import Customers,customer_schema,customers_schema
from ..models.car import Cars,car_schema,cars_schema
from ..models.customer_car import Customers_cars,customerCar_schema,customerCars_schema
from ..models.customer_item import Customer_items,customerItem_schema,customerItems_schema

from ..models.final_checklist import Final_Checklists,finalChecklist_schema,finalChecklists_schema
from ..models.initial_checklist import Initial_Checklists,initialChecklist_schema,initialChecklists_schema
from datetime import date

voucher_route=Blueprint('voucher_route',__name__)


@voucher_route.route('/voucher/get',methods=['GET'])
def get_vouchers():
	# all_vouchers=Vouchers.query.all()
	# results=vouchers_schema.dump(all_vouchers)
	# return jsonify(results)

	customerCar_array={"customer":"","car":""}
	voucher_array=[]

	vouchers = db.session.query(Vouchers, Customers_cars,Vouchers_Payment).join(Customers_cars,Vouchers_Payment).all()
	for voucher, customer_car,voucher_payment in vouchers:
		voucher_result=voucher_schema.dump(voucher)
		customer_cars = db.session.query(Customers_cars, Customers, Cars).filter(Customers_cars.id==voucher.customerCar_id).join(Customers).join(Cars).all()
		for customer_car, customer, car in customer_cars:
			customer_result=customer_schema.dump(customer)
			car_result=car_schema.dump(car)
			customerCar_array["customer"]=customer_result
			customerCar_array["car"]=car_result
			voucher_result["customerCar_id"]=customerCar_array.copy()
		voucher_result["payment"]=voucherPayment_schema.dump(voucher_payment)
		voucher_array.append(voucher_result)
	return jsonify(voucher_array)


@voucher_route.route('/voucher/get/<id>/',methods=['GET'])
def post_details(id):
	customerCar_array={"customer":"","car":""}
	dist={"voucher":""}

	vouchers = db.session.query(Vouchers, Customers_cars).filter(Vouchers.id==id).join(Customers_cars).all()
	for voucher, customer_car in vouchers:
		customer_cars = db.session.query(Customers_cars, Customers, Cars).filter(Customers_cars.id==voucher.customerCar_id).join(Customers).join(Cars).all()
		for customer_car, customer, car in customer_cars:
			customer_result=customer_schema.dump(customer)
			car_result=car_schema.dump(car)
			customerCar_array["customer"]=customer_result
			customerCar_array["car"]=car_result
		voucher_result=voucher_schema.dump(voucher)
		voucher_result["customerCar_id"]=customerCar_array
		dist["voucher"]=voucher_result

	return jsonify(dist)

@voucher_route.route('/voucher/add/',methods=['POST'])
def add_voucheremployee():
	customerCar_id=request.json['customerCar_id']
	initChecklist_id=request.json['initChecklist_id']
	finalChecklist_id=request.json['finalChecklist_id']
	total=request.json['total']

	voucher=Vouchers(customerCar_id,initChecklist_id,finalChecklist_id,total)
	db.session.add(voucher)
	db.session.commit()
	return voucher_schema.jsonify(voucher)


@voucher_route.route('/voucher/update/<id>/',methods=['PUT'])
def update_voucheremployee(id):
	voucher=Vouchers.query.get(id)
	
	customerCar_id=request.json['customerCar_id']
	initChecklist_id=request.json['initChecklist_id']
	finalChecklist_id=request.json['finalChecklist_id']
	total=request.json['total']

	voucher.customerCar_id=customerCar_id
	voucher.initChecklist_id=initChecklist_id
	voucher.finalChecklist_id=finalChecklist_id
	voucher.total=total

	db.session.commit()
	return voucher_schema.jsonify(voucher)

@voucher_route.route('/voucher/delete/<id>/',methods=['DELETE'])
def delete_voucheremployee(id):
	voucher=Vouchers.query.get(id)

	db.session.delete(voucher)
	db.session.commit()

	return voucher_schema.jsonify(voucher)

@voucher_route.route('/voucher/customervoucher/<customerID>',methods=['GET'])
def get_customervoucher(customerID):
	customerCar_array={"customer":"","car":""}
	voucher_array=[]
	customerCars = db.session.query(Customers_cars,Customers,Cars).filter(Customers_cars.customer_id==customerID).join(Customers).join(Cars).all()
	for customerCar,customer, car in customerCars:
		customer_result=customer_schema.dump(customer)
		car_result=car_schema.dump(car)
		customerCar_array["customer"]=customer_result
		customerCar_array["car"]=car_result
		vouchers=db.session.query(Vouchers,Vouchers_Payment).filter(Vouchers.customerCar_id==customerCar.id).join(Vouchers_Payment).all()
		for voucher,voucher_payment in vouchers:
			voucher_result=voucher_schema.dump(voucher)
			voucher_result["customerCar_id"]=customerCar_array.copy()
			voucher_result["payment"]=voucherPayment_schema.dump(voucher_payment)
			voucher_array.append(voucher_result)
	return jsonify(voucher_array)

@voucher_route.route('/voucher/sales/<day>/<month>/<year>/',methods=['GET'])
def get_sales(day,month,year):
	total_sale=0
	voucher_Date=date(year=int(year),month=int(month),day=int(day))

	# star_Date=date(year=int(2021),month=int(1),day=int(1))
	# end_Date=date(year=int(2021),month=int(12),day=int(31))

	# query_vouchers=Vouchers.query.filter(Vouchers.date<=end_Date).filter(Vouchers.date>=star_Date).all()
	query_vouchers=Vouchers.query.filter(Vouchers.date==voucher_Date).all()
	for voucher in query_vouchers:
		total_sale+=voucher.total
	

	
	#daily sales
	# voucherDetails=[]
	# dist={"voucher_serviceitem":voucherDetails}
	
	# voucher_date=d_truncated
	# query_vouchers=Vouchers.query.filter(Vouchers.date==voucher_date).all()
	# for query_voucher in query_vouchers:
	# 	voucher_result=voucher_schema.dump(query_voucher)
	# 	vouchers_serviceItems = db.session.query(Vouchers_servicesitems, Services_items).filter(Vouchers_servicesitems.voucher_id==voucher_result["id"]).join(Services_items).all()
	# 	for vouchers_serviceItem, service_item in vouchers_serviceItems:
	# 		serviceItems = db.session.query(Services_items,Items.id!=None,Services,Customer_items).filter(Services_items.id==vouchers_serviceItem.serviceItem_id,Items!=None).outerjoin(Items).join(Services).outerjoin(Customer_items).all()
	# 		for service_item, item,customer_item,service in serviceItems:
	# 			item_result=item_schema.dump(item)
	# 			service_result=service_schema.dump(service)
	# 			customerItem_result=customerItem_schema.dump(customer_item)
	# 		serviceitem_result=serviceItem_schema.dump(service_item)
	# 		serviceitem_result['item_id']=item_result
	# 		serviceitem_result['service_id']=service_result
	# 		voucherDetail_result=voucherServiceItem_schema.dump(vouchers_serviceItem)
	# 		voucherDetail_result['serviceItem_id']=serviceitem_result
	# 		voucherDetails.append(voucherDetail_result)
		# print(serviceitem_result)

	# print(dist)

	return jsonify(total_sale)

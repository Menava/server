from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,ma,getTodayDate,getTimeWindow
from ..models.voucher import Vouchers,voucher_schema,vouchers_schema
from ..models.voucher_outsource import Vouchers_outsources,voucheroutsource_schema,voucheroutsources_schema
from ..models.service import Services,service_schema,services_schema
from ..models.voucher_serviceitem import Vouchers_servicesitems,voucherServiceItem_schema,voucherServiceItems_schema
from ..models.voucher_outsource import Vouchers_outsources,voucheroutsource_schema,voucheroutsources_schema
from ..routes.serviceplaceServiceItems_route import loop_serviceItem
from ..models.voucher_payment import Vouchers_Payment,voucherPayment_schema,voucherPayments_schema
from ..models.service_item import Services_items,serviceItem_schema,serviceItems_schema
from ..models.item import Items,item_schema,items_schema
from ..models.item_purchase import Items_Purchase,itemPurchase_schema,itemPurchases_schema
from ..models.item_payment import itemPayment_schema,itemPayments_schema

from ..models.general_purchase import General_Purchases,generalPurchase_schema,generalPurchases_schema
from ..models.general_income import General_Incomes,generalIncome_schema,generalIncomes_schema
from ..models.employee_payroll import Employees_Payroll,employeePayroll_schema,employeePayrolls_schema

from ..models.customer import Customers,customer_schema,customers_schema
from ..models.car import Cars,car_schema,cars_schema
from ..models.customer_car import Customers_cars,customerCar_schema,customerCars_schema
from ..models.customer_item import Customer_items,customerItem_schema,customerItems_schema

from ..models.final_checklist import Final_Checklists,finalChecklist_schema,finalChecklists_schema
from ..models.initial_checklist import Initial_Checklists,initialChecklist_schema,initialChecklists_schema
from datetime import date
from sqlalchemy import func

voucher_route=Blueprint('voucher_route',__name__)


@voucher_route.route('/voucher/get',methods=['GET'])
def get_vouchers():
	customerCar_array={"customer":"","car":""}
	voucher_array=[]

	vouchers = db.session.query(Vouchers, Customers_cars,Vouchers_Payment).join(Customers_cars,Vouchers_Payment).order_by(Vouchers.date.desc()).all()
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

@voucher_route.route('/voucher/sales/weekly', methods=['GET'])
def get_dashboard():
	return_dict={'Vouche Weekly Chart':''}
	voucherChart_array=[]
	vChart_data={}
	voucher_groupby=db.session.query(Vouchers.date,func.sum(Vouchers.total).label('Total')).filter(Vouchers.date>getTodayDate() - getTimeWindow('week')).group_by(Vouchers.date).all()
	for i in voucher_groupby:
		vChart_data["Date"]=i[0]
		vChart_data['Total']=i[1]
		voucherChart_array.append(vChart_data.copy())
	
	return_dict['Vouche Weekly Chart']=voucherChart_array
	return jsonify(return_dict)

@voucher_route.route('/voucher/sales/<option>',methods=['GET'])
def get_sales(option):
	voucher_count=0
	revenue=0
	etotal=0
	gtotal=0
	gincome_total=0
	vsource_total=0
	purchase_total=0
	gpChart_array=[]
	gp_data={}
	return_dict={'num of sales':'','income':'','revenue':'','total expense':'','general purchase':'','emp salary':'','gp_chart':'','Investment':''}
	if(option=='today'):
		query_result=db.session.query(Vouchers,Vouchers_Payment).join(Vouchers_Payment).filter(Vouchers.date==getTodayDate()).all()
		all_voucherOutsources=Vouchers_outsources.query.filter(Vouchers_outsources.paid_date==getTodayDate(),Vouchers_outsources.status==True).all()
		all_generalpurchases=General_Purchases.query.filter(General_Purchases.purchase_date==getTodayDate()).all()
		all_generalincomes=General_Incomes.query.filter(General_Incomes.income_date==getTodayDate()).all()
		all_employeePay=Employees_Payroll.query.filter(Employees_Payroll.paid_date==getTodayDate()).all()
		all_itemPayments=db.session.query(Items_Purchase,Items).filter(Items_Purchase.purchase_date==getTodayDate(),Items_Purchase.status==False).join(Items).all()
		purchase_total=getItemPurchase(all_itemPayments,option)
		gp_groupby=db.session.query(General_Purchases.purchase_type,func.sum(General_Purchases.total).label('Total')).filter(General_Purchases.purchase_date==getTodayDate()).group_by(General_Purchases.purchase_type).all()
	if(option=='week'):
		query_result=db.session.query(Vouchers,Vouchers_Payment).join(Vouchers_Payment).filter(Vouchers.date>getTodayDate() - getTimeWindow('week')).all()
		all_voucherOutsources=Vouchers_outsources.query.filter(Vouchers_outsources.paid_date>getTodayDate()- getTimeWindow('week'),Vouchers_outsources.status==True).all()
		all_generalpurchases=General_Purchases.query.filter(General_Purchases.purchase_date>getTodayDate() - getTimeWindow('week')).all()
		all_generalincomes=General_Incomes.query.filter(General_Incomes.income_date>getTodayDate() - getTimeWindow('week')).all()
		all_employeePay=Employees_Payroll.query.filter(Employees_Payroll.paid_date>getTodayDate() - getTimeWindow('week')).all()
		all_itemPayments=db.session.query(Items_Purchase,Items).filter(Items_Purchase.purchase_date>getTodayDate() - getTimeWindow('week'),Items_Purchase.status==False).join(Items).all()
		purchase_total=getItemPurchase(all_itemPayments,option)
		gp_groupby=db.session.query(General_Purchases.purchase_type,func.sum(General_Purchases.total).label('Total')).filter(General_Purchases.purchase_date>getTodayDate() - getTimeWindow('week')).group_by(General_Purchases.purchase_type).all()
	if(option=='month'):
		query_result=db.session.query(Vouchers,Vouchers_Payment).join(Vouchers_Payment).filter(Vouchers.date>getTodayDate() - getTimeWindow('month')).all()
		all_voucherOutsources=Vouchers_outsources.query.filter(Vouchers_outsources.paid_date>getTodayDate() - getTimeWindow('month'),Vouchers_outsources.status==True).all()
		all_generalpurchases=General_Purchases.query.filter(General_Purchases.purchase_date>getTodayDate() - getTimeWindow('month')).all()
		all_generalincomes=General_Incomes.query.filter(General_Incomes.income_date>getTodayDate() - getTimeWindow('month')).all()
		all_employeePay=Employees_Payroll.query.filter(Employees_Payroll.paid_date>getTodayDate() - getTimeWindow('month')).all()
		all_itemPayments=db.session.query(Items_Purchase,Items).filter(Items_Purchase.purchase_date>getTodayDate() - getTimeWindow('month'),Items_Purchase.status==False).join(Items).all()
		purchase_total=getItemPurchase(all_itemPayments,option)
		gp_groupby=db.session.query(General_Purchases.purchase_type,func.sum(General_Purchases.total).label('Total')).filter(General_Purchases.purchase_date>getTodayDate() - getTimeWindow('month'),Items_Purchase.status==False).group_by(General_Purchases.purchase_type).all()
	if(option=='all'):
		query_result=db.session.query(Vouchers,Vouchers_Payment).join(Vouchers_Payment).all()
		all_voucherOutsources=Vouchers_outsources.query.filter(Vouchers_outsources.status==True).all()
		all_generalpurchases=General_Purchases.query.all()
		all_generalincomes=General_Incomes.query.all()
		all_employeePay=Employees_Payroll.query.all()
		all_itemPayments=db.session.query(Items_Purchase,Items).filter(Items_Purchase.status==False).join(Items).all()
		purchase_total=getItemPurchase(all_itemPayments,option)
		gp_groupby=db.session.query(General_Purchases.purchase_type,func.sum(General_Purchases.total).label('Total')).group_by(General_Purchases.purchase_type).all()
	
	for voucher,voucherPayment in query_result:
		voucher.total=voucherPayment.paid_amount
		revenue+=voucher.total
		voucher_count+=1

	for i in all_generalpurchases:
		gtotal+=i.total

	for i in all_generalincomes:
		gincome_total+=i.amount

	for i in all_employeePay:
		etotal+=i.salary_amount
	
	for i in gp_groupby:
		gp_data["Category"]=i[0]
		gp_data['Total']=i[1]
		gpChart_array.append(gp_data.copy())
	
	for i in all_voucherOutsources:
		vsource_total+=i.total

	revenue+=gincome_total
	total_expense=etotal+gtotal+vsource_total
	income=revenue-total_expense

	
	return_dict['revenue']=revenue
	return_dict['num of sales']=voucher_count
	return_dict['total expense']=total_expense
	return_dict['income']=income
	return_dict['general purchase']=gtotal
	return_dict['emp salary']=etotal
	return_dict['gp_chart']=gpChart_array
	return_dict['Investment']=purchase_total
	
	return jsonify(return_dict)

def getItemPurchase(all_itemPayments,option):
	purchase_total=0
	for item_purchase,item in all_itemPayments:
		print('item_purchase',itemPurchase_schema.dump(item_purchase))
		if(item.refundable==True):
			item_purchase.quantity_received=getItemQty(item_purchase.item_id,option)
		# total=item_purchase.quantity_received*item_purchase.unit_price
		# purchase_total+=total
	return purchase_total

def getItemQty(id,option):
	itm_qty=0
	temp_receive=0
	temp_refund=0
	result_count=db.session.query(Items_Purchase).filter(Items_Purchase.item_id==id).filter(Items_Purchase.purchase_date>getTodayDate() - getTimeWindow('week')).order_by(Items_Purchase.id.desc()).count()
	result=db.session.query(Items_Purchase).filter(Items_Purchase.item_id==id).order_by(Items_Purchase.id.desc()).limit(result_count+1).all()
	print(type(result))
	for i in result:
		print('i',itemPurchase_schema.dump(i))
		
	
	# if((result.count())!=2):
	# 	itm_qty=result[0].quantity_received
	# else:
	# 	diff_time=result[0].purchase_date-result[1].purchase_date
	# 	print(diff_time)
	# 	if(option=='today'):
	# 		pass
	# 		# itm_qty=result[0].quantity_received-result[1].refund_quantity
	# 	if(option=='week'):
	# 		pass
	# 	if(option=='month'):
	# 		pass
	# 	if(option=='today'):
	# 		pass
	# 	if(option=='all'):
	# 		pass
	# 	itm_qty=result[0].quantity_received-result[1].refund_quantity

	return itm_qty
	
@voucher_route.route('/itemprofit/<option>', methods=['GET'])
def get_itemprofit(option):
	service_list={}
	item_list={}

	service_array=[]
	item_array=[]

	service_total=0
	item_total=0
	item_ProfitTotal=0
	voucher_total=0
	outsource_total=0

	return_dict={'service':'','item':'','service total':'','item total':'','item profit total':''}
	if(option=='today'):
		vouchers_result=Vouchers.query.filter(Vouchers.date==getTodayDate()).all()
	if(option=='week'):
		vouchers_result=Vouchers.query.filter(Vouchers.date>getTodayDate() - getTimeWindow('week')).all()
	if(option=='month'):
		vouchers_result=Vouchers.query.filter(Vouchers.date>getTodayDate() - getTimeWindow('month')).all()
	if(option=='all'):
		vouchers_result=Vouchers.query.all()
	for voucher in vouchers_result:
		voucher_total+=voucher.total
		service_detail=loop_serviceItem(voucher.id)
		for each_line in service_detail:
			service_collection=Service_collection(each_line["service"]["service_type"],each_line["service"]["service_price"],1)
			
			if each_line["service"]["id"] not in service_list:
				service_list[each_line["service"]["id"]]=service_collection
			else:
				temp_serviceCollection=service_list[each_line["service"]["id"]]
				temp_serviceCollection.price+=service_collection.price
				temp_serviceCollection.quantity+=1
				service_list[each_line["service"]["id"]]=temp_serviceCollection
			service_total+=each_line["service"]["service_price"]

			for each_item in each_line["items"]:
				item_purchase=Items_Purchase.query.filter(Items_Purchase.item_id==each_item["id"],Items_Purchase.status==False).order_by(Items_Purchase.id.desc()).first()
				item_totalPrice=each_item["price"]*each_item["quantity"]
				item_profit=item_totalPrice-(item_purchase.unit_price*each_item["quantity"])
				item_profitPercent="%.2f" %((item_profit/(item_purchase.unit_price*each_item["quantity"]))*100)
				item_collection=Item_collection(each_item["name"],item_purchase.unit_price,item_totalPrice,each_item["quantity"],item_profit,item_profitPercent)

				if each_item["id"] not in item_list:
					item_list[each_item["id"]]=item_collection
				else:
					temp_itemCollection=item_list[each_item["id"]]
					temp_itemCollection.price+=item_collection.price
					temp_itemCollection.quantity+=item_collection.quantity
					temp_itemCollection.profit=temp_itemCollection.price-(temp_itemCollection.buy_price*temp_itemCollection.quantity)
					temp_itemCollection.profit_percent="%.2f" % (temp_itemCollection.profit/(temp_itemCollection.buy_price*temp_itemCollection.quantity)*100)
					item_list[each_item["id"]]=temp_itemCollection
				item_total+=item_totalPrice
				item_ProfitTotal+=item_profit

	serviceValue_list=list(service_list.values())
	itemValue_list=list(item_list.values())

	for i in service_list.values():
		service_array.append(i.getDict())
	
	for i in item_list.values():
		item_array.append(i.getDict())
	
	return_dict['service']=service_array
	return_dict['item']=item_array
	return_dict['service total']=service_total
	return_dict['item total']=item_total
	return_dict['item profit total']=item_ProfitTotal
	
	return jsonify(return_dict)



class Service_collection():
  def __init__(self,name, price, quantity):
    self.name=name
    self.price = price
    self.quantity = quantity
  def __str__(self):
    return f'({self.name},{self.price},{self.quantity})'

  def getDict(self):
    dic={"name":self.name,"price":self.price,"quantity":self.quantity}
    return dic



class Item_collection():
  def __init__(self, name,buy_price,price,quantity,profit,profit_percent):
    self.name=name
    self.buy_price=buy_price
    self.price = price
    self.quantity = quantity
    self.profit = profit
    self.profit_percent=profit_percent
  
  def __str__(self):
    return f'({self.name},{self.buy_price},{self.price},{self.quantity},{self.profit},{self.profit_percent})'

  def getDict(self):
    dic={"name":self.name,"buy_price":self.buy_price,"total_price":self.price,"total_quantity":self.quantity,"profit":self.profit,"profit_percent":self.profit_percent}
    return dic
	
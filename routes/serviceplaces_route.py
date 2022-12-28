from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.service_place import ServicePlaces,servicePlace_schema,servicePlaces_schema
from ..models.customer_car import Customers_cars,customerCar_schema,customerCars_schema
from ..models.customer import Customers,customer_schema,customers_schema
from ..models.car import Cars,car_schema,cars_schema
from ..models.customer_car import Customers_cars,customerCar_schema,customerCars_schema
from ..models.initial_checklist import Initial_Checklists,initialChecklist_schema,initialChecklists_schema
from ..models.init_checklist_image import Init_Checklist_Images,initChecklistImage_schema,initChecklistImages_schema
from ..models.servicePlace_serviceitem import ServicePlaces_servicesitems,serviceplaceServiceItem_schema,serviceplaceServiceItems_schema
from ..models.servicePlace_employee import ServicePlaces_employees,serviceplaceEmployee_schema,serviceplaceEmployees_schema
import base64,os,string,random

serviceplace_route=Blueprint('serviceplace_route',__name__)


@serviceplace_route.route('/serviceplace/get',methods=['GET'])
def get_serviceplaces():
	customerCar_array={"customer":"","car":""}
	Initial_array={"Initial_checkList":"","Initial_Image":""}
	serviceplace_array=[]

	serviceplaces = db.session.query(ServicePlaces, Customers_cars,Initial_Checklists).outerjoin(Customers_cars,Initial_Checklists).all()
	for serviceplace, customer_car,initial_checklist in serviceplaces:
		serviceplace_result=servicePlace_schema.dump(serviceplace)
		customer_cars = db.session.query(Customers_cars, Customers, Cars).filter(Customers_cars.id==serviceplace.customerCar_id).join(Customers).join(Cars).all()
		for customer_car, customer, car in customer_cars:
			customer_result=customer_schema.dump(customer)
			car_result=car_schema.dump(car)
			customerCar_array["customer"]=customer_result
			customerCar_array["car"]=car_result
			serviceplace_result["customerCar_id"]=customerCar_array.copy()
		initial_checklists=db.session.query(Initial_Checklists,Init_Checklist_Images ).filter(Initial_Checklists.id==serviceplace.initChecklist_id).join(Init_Checklist_Images).all()
		for initcheck, initImage in initial_checklists:
			init_result=initialChecklist_schema.dump(initcheck)
			initImage_result=initChecklistImage_schema.dump(initImage)
			Initial_array["Initial_checkList"]=init_result
			Initial_array["Initial_Image"]=initImage_result
			serviceplace_result["initChecklist_id"]=Initial_array.copy()
		serviceplace_array.append(serviceplace_result)

	return jsonify(serviceplace_array)


@serviceplace_route.route('/serviceplace/get/<id>/',methods=['GET'])
def post_details(id):
	dist={"serviceplaces":"","serviceplace_Employees":"","serviceplace_ServiceItems":""}
	customerCar_array={"customer":"","car":""}
	serviceplaceServiceItem_array=[]
	serviceplaceEmployee_array=[]
	
	serviceplaces = db.session.query(ServicePlaces, Customers_cars).filter(ServicePlaces.id==id).join(Customers_cars).all()
	for serviceplace, customer_car in serviceplaces:
		customer_cars = db.session.query(Customers_cars, Customers, Cars).filter(Customers_cars.id==serviceplace.customerCar_id).join(Customers).join(Cars).all()
		for customer_car, customer, car in customer_cars:
			customer_result=customer_schema.dump(customer)
			car_result=car_schema.dump(car)
			customerCar_array["customer"]=customer_result
			customerCar_array["car"]=car_result
		serviceplace_result=servicePlace_schema.dump(serviceplace)
		serviceplace_result["customerCar_id"]=customerCar_array
		dist["serviceplaces"]=serviceplace_result
	
	
	serviceplace_serviceitems=db.session.query(ServicePlaces_servicesitems,ServicePlaces).filter(ServicePlaces_servicesitems.servicePlace_id==id).join(ServicePlaces).all()
	for serviceplace_serviceitem,serviceplace in serviceplace_serviceitems:
		serviceplaceItem_result=serviceplaceServiceItem_schema.dump(serviceplace_serviceitem)
		serviceplaceItem_result["servicePlace_id"]=serviceplace.name
		serviceplaceServiceItem_array.append(serviceplaceItem_result)
	
	dist["serviceplace_ServiceItems"]=serviceplaceServiceItem_array.copy()

	serviceplace_employees=ServicePlaces_employees.query.filter(ServicePlaces_employees.servicePlace_id==id).all()
	for serviceplace_employee in serviceplace_employees:
		serviceplaceEmployee_result=serviceplaceEmployee_schema.dump(serviceplace_employee)
		serviceplaceEmployee_array.append(serviceplaceEmployee_result)
	
	dist["serviceplace_Employees"]=serviceplaceEmployee_array.copy()
	return jsonify(dist)

@serviceplace_route.route('/serviceplace/add/',methods=['POST'])
def add_serviceplace():
	name=request.json['name']
	customerCar_id=request.json['customerCar_id']
	initChecklist_id=request.json['initChecklist_id']
	state=request.json['state']
	status=request.json['status']

	if(name=='Other' or name=='Waiting'):
		name=name+"#"+randomName(3)
	else:
		customerCar_id=None
		initChecklist_id=None

	serviceplace=ServicePlaces(name,customerCar_id,initChecklist_id,state,status)
	db.session.add(serviceplace)
	db.session.commit()
	return servicePlace_schema.jsonify(serviceplace)

@serviceplace_route.route('/serviceplace/update/v2/<id>/<newID>',methods=['PUT'])
def update_serviceplacev2(id,newID):
	serviceplace=ServicePlaces.query.get(id)
	new_serviceplace=ServicePlaces.query.get(newID)



	new_serviceplace.customerCar_id=serviceplace.customerCar_id
	new_serviceplace.initChecklist_id=serviceplace.initChecklist_id
	new_serviceplace.state=0
	new_serviceplace.status='On Progress'

	db.session.commit()
	return servicePlace_schema.jsonify(serviceplace)

@serviceplace_route.route('/serviceplace/update/<id>/',methods=['PUT'])
def update_serviceplace(id):
	serviceplace=ServicePlaces.query.get(id)
	
	name=request.json['name']
	customerCar_id=request.json['customerCar_id']
	initChecklist_id=request.json['initChecklist_id']
	state=request.json['state']
	status=request.json['status']

	serviceplace.name=name
	serviceplace.customerCar_id=customerCar_id
	serviceplace.initChecklist_id=initChecklist_id
	serviceplace.state=state
	serviceplace.status=status

	db.session.commit()
	return servicePlace_schema.jsonify(serviceplace)

@serviceplace_route.route('/serviceplace/delete/<id>/',methods=['PUT'])
def delete_servicePlace(id):
	dist={"service_place":"","serviceplace_Employees":"","serviceplace_ServiceItems":""}

	serviceplace=ServicePlaces.query.get(id)
	serviceplace_result=servicePlace_schema.dump(serviceplace)
	dist["service_place"]=serviceplace_result

	dist["serviceplace_ServiceItems"]=delete_item(id)
	dist["serviceplace_Employees"]=delete_employees(id)

	serviceplace.customerCar_id=None
	serviceplace.initChecklist_id=None
	serviceplace.state=0
	serviceplace.status="Free"
	
	db.session.add(serviceplace)
	db.session.commit()
	return jsonify(dist)

@serviceplace_route.route('/serviceplace/real-delete/<id>/',methods=['DELETE'])
def delete_servicePlace_real(id):
	serviceplace=ServicePlaces.query.get(id)

	db.session.delete(serviceplace)
	db.session.commit()

	return servicePlace_schema.jsonify(serviceplace)

def delete_item(id):
	serviceplaceServiceItem_array=[]
	serviceplace_serviceitems=db.session.query(ServicePlaces_servicesitems,ServicePlaces).filter(ServicePlaces_servicesitems.servicePlace_id==id).join(ServicePlaces).all()
	for serviceplace_serviceitem,serviceplace in serviceplace_serviceitems:
		serviceplaceItem_result=serviceplaceServiceItem_schema.dump(serviceplace_serviceitem)
		serviceplaceItem_result["servicePlace_id"]=serviceplace.name
		serviceplaceServiceItem_array.append(serviceplaceItem_result)
		db.session.delete(serviceplace_serviceitem)
		db.session.commit()

	return serviceplaceServiceItem_array.copy()

def delete_employees(id):
	serviceplaceEmployee_array=[]
	serviceplace_employees=ServicePlaces_employees.query.filter(ServicePlaces_employees.servicePlace_id==id).all()
	for serviceplace_employee in serviceplace_employees:
		serviceplaceEmployee_result=serviceplaceEmployee_schema.dump(serviceplace_employee)
		serviceplaceEmployee_array.append(serviceplaceEmployee_result)
		db.session.delete(serviceplace_employee)
		db.session.commit()
	
	return serviceplaceEmployee_array.copy()

def randomName(length):
    # With combination of lower and upper case
    result_digits = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, length)])
    # print random string
    return 	result_digits
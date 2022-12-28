from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.initial_checklist import Initial_Checklists,initialChecklist_schema,initialChecklists_schema
import base64,os,string,random

from ..config import imagePath,init_customerfolder,init_employeefolder
from .googleService_route import insert_ToDrive,delete_fileDrive

initcheck_route=Blueprint('initcheck_route',__name__)

employeeFolder_id=init_employeefolder
customerFolder_id=init_customerfolder

@initcheck_route.route('/initchecklist/get',methods=['GET'])
def get_initChecklist():
	initialChecklists=Initial_Checklists.query.all()
	results=initialChecklists_schema.dump(initialChecklists)
	return jsonify(results)


@initcheck_route.route('/initchecklist/get/<id>/',methods=['GET'])
def post_details(id):
	initialChecklist=Initial_Checklists.query.get(id)
	return initialChecklist_schema.jsonify(initialChecklist)



@initcheck_route.route('/initchecklist/add/',methods=['POST'])
def add_initChecklist():
	try:
		employee_sign=request.json['employee_sign']
		customer_sign=request.json['customer_sign']
		notes=request.json['notes']

		employee_signName,employee_path = saveEmployeeSign(employee_sign)
		customer_signName,customer_path = saveCustomerSign(customer_sign)

		initialChecklist=Initial_Checklists(employee_signName,employee_path,customer_signName,customer_path,notes)
		db.session.add(initialChecklist)
		db.session.commit()
	except:
		return 'Something went wrong',500
	else:
		return initialChecklist_schema.jsonify(initialChecklist)


@initcheck_route.route('/initchecklist/update/<id>/',methods=['PUT'])
def update_initChecklist(id):
	initialChecklist=Initial_Checklists.query.get(id)

	employee_sign=request.json['employee_sign']
	customer_sign=request.json['customer_sign']
	notes=request.json['notes']
	

	initialChecklist.employee_sign=employee_sign
	initialChecklist.customer_sign=customer_sign
	initialChecklist.notes=notes

	db.session.commit()
	return initialChecklist_schema.jsonify(initialChecklist)

@initcheck_route.route('/initchecklist/delete/<id>/',methods=['DELETE'])
def delete_initChecklist(id):
	initialChecklist=Initial_Checklists.query.get(id)

	db.session.delete(initialChecklist)
	db.session.commit()

	return initialChecklist_schema.jsonify(initialChecklist)

def saveEmployeeSign(employee_sign):
	encoded_file=employee_sign.split(",")[1]
	decoded_file=base64.b64decode(encoded_file)
	
	file_name =randomName(8)+".png"	
	imageFile = os.path.join(imagePath, file_name)
	file = open(imageFile,'wb')
	file.write(decoded_file)
	file.close()

	file_id=insert_ToDrive(file_name,imagePath,employeeFolder_id)

	return file_name,file_id

def saveCustomerSign(customer_sign):
	encoded_file=customer_sign.split(",")[1]
	decoded_file=base64.b64decode(encoded_file)
	
	file_name = randomName(8)+".png"	
	imageFile = os.path.join(imagePath, file_name)
	file = open(imageFile,'wb')
	file.write(decoded_file)
	file.close()

	file_id=insert_ToDrive(file_name,imagePath,customerFolder_id)

	return file_name,file_id

def randomName(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return 	result_str
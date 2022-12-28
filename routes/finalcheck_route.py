from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
from ..models.final_checklist import Final_Checklists,finalChecklist_schema,finalChecklists_schema
import base64,os,string,random

from ..config import imagePath,final_employeefolder,final_customerfolder
from .googleService_route import insert_ToDrive,delete_fileDrive

finalcheck_route=Blueprint('finalcheck_route',__name__)

employeeFolder_id=final_employeefolder
customerFolder_id=final_customerfolder

@finalcheck_route.route('/finalchecklist/get',methods=['GET'])
def get_finalChecklist():
	finalChecklists=Final_Checklists.query.all()
	results=finalChecklists_schema.dump(finalChecklists)
	return jsonify(results)


@finalcheck_route.route('/finalchecklist/get/<id>/',methods=['GET'])
def post_details(id):
	finalChecklist=Final_Checklists.query.get(id)
	return finalChecklist_schema.jsonify(finalChecklist)



@finalcheck_route.route('/finalchecklist/add/',methods=['POST'])
def add_finalChecklist():
	try:
		employee_sign=request.json['employee_sign']
		customer_sign=request.json['customer_sign']
		notes=request.json['notes']
		customer_rating=request.json['customer_rating']

		employee_signName,employee_path = saveEmployeeSign(employee_sign)
		customer_signName,customer_path = saveCustomerSign(customer_sign)

		finalChecklist=Final_Checklists(employee_signName,employee_path,customer_signName,customer_path,notes,customer_rating)
		db.session.add(finalChecklist)
		db.session.commit()
	except:
		return 'Something went wrong',500
	else:
		return finalChecklist_schema.jsonify(finalChecklist)


@finalcheck_route.route('/finalchecklist/update/<id>/',methods=['PUT'])
def update_finalChecklist(id):
	finalChecklist=Final_Checklists.query.get(id)

	employee_sign=request.json['employee_sign']
	customer_sign=request.json['customer_sign']
	notes=request.json['notes']
	customer_rating=request.json['customer_rating']

	finalChecklist.employee_sign=employee_sign
	finalChecklist.customer_sign=customer_sign
	finalChecklist.notes=notes
	finalChecklist.customer_rating=customer_rating

	db.session.commit()
	return finalChecklist_schema.jsonify(finalChecklist)

@finalcheck_route.route('/finalchecklist/delete/<id>/',methods=['DELETE'])
def delete_finalChecklist(id):
	finalChecklist=Final_Checklists.query.get(id)

	db.session.delete(finalChecklist)
	db.session.commit()

	return finalChecklist_schema.jsonify(finalChecklist)

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
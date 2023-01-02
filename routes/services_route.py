from flask import jsonify,request,render_template,redirect,Blueprint
from googleapiclient.http import MediaFileUpload

from ..models.service import Services,service_schema,services_schema

from ..extensions import db
from ..config import imagePath,service_folder
from .googleService_route import insert_ToDrive,delete_fileDrive

import os

folder_id=service_folder

service_route=Blueprint('service_route',__name__)

@service_route.route('/service/get',methods=['GET'])
def get_services():
	all_services=Services.query.filter(Services.hidden==False).all()
	results=services_schema.dump(all_services)
	return jsonify(results)


@service_route.route('/service/get/<id>/',methods=['GET'])
def post_details(id):
	service=Services.query.get(id)
	return service_schema.jsonify(service)



@service_route.route('/service/add/',methods=['POST'])
def add_service():
	try:
		files=request.files
		image = files.get('file')
		service_type = request.form.get('service_type')
		service_price = request.form.get('service_price')
		service_detail = request.form.get('service_detail')
		image.save(os.path.join(imagePath,image.filename))

		file_id=insert_ToDrive(image.filename,imagePath,folder_id)
		service=Services(service_type,image.filename,file_id,service_price,service_detail)
		db.session.add(service)
		db.session.commit()
	except Exception as e:
		print(e)
		return "something went wrong",500
	else:
		return service_schema.jsonify(service)

@service_route.route('/service/update/<id>/',methods=['PUT'])
def update_service(id):
	service=Services.query.get(id)
	try:
		files=request.files
		if files:
			# os.remove(os.path.join(imagePath, service.service_imageName))
			delete_fileDrive(service.service_imagePath)
			image = files.get('file')
			image.save(os.path.join(imagePath,image.filename))
			file_id=insert_ToDrive(image.filename,imagePath,folder_id)
			service.service_imageName=image.filename
			service.service_imagePath=file_id
		else:
			image=request.form.get('file')
			service.service_imageName=service.service_imageName

		service_type = request.form.get('service_type')
		service_price = request.form.get('service_price')
		service_detail = request.form.get('service_detail')
		# hidden=request.form.get('hidden')
		

		service.service_type=service_type
		service.service_price=service_price
		service.service_detail=service_detail
		# service.hidden=hidden

		db.session.commit()
	
	except:
		return 'something went wrong',500
	else:
		return service_schema.jsonify(service)

@service_route.route('/service/delete/<id>/',methods=['PUT'])
def delete_service(id):
	service=Services.query.get(id)

	service.hidden=True
	db.session.commit()

	return service_schema.jsonify(service)
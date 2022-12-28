from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,ma
import os
from ..models.initial_checklist import Initial_Checklists,initialChecklist_schema,initialChecklists_schema
from ..models.init_checklist_image import Init_Checklist_Images,initChecklistImage_schema,initChecklistImages_schema
import json
from ..config import imagePath,init_imageFolder
from .googleService_route import insert_ToDrive,delete_fileDrive

initialimage_route=Blueprint('initialImage_route',__name__)

folder_id=init_imageFolder

@initialimage_route.route('/initialchecklist/image/get',methods=['GET'])
def get_initImages():
	all_initialImages=Init_Checklist_Images.query.all()
	results=initChecklistImages_schema.dump(all_initialImages)
	return jsonify(results)


@initialimage_route.route('/initialchecklist/image/get/<id>/',methods=['GET'])
def post_details(id):
	initial_images=Init_Checklist_Images.query.filter(Init_Checklist_Images.intChecklist_id==id).all()
	return initChecklistImages_schema.jsonify(initial_images)
	
@initialimage_route.route('/initialchecklist/image/upload/',methods=['POST'])
def upload_finalImage():
	file_status=False
	try:
		uploaded_files = request.files.getlist("file")
		if(uploaded_files):
			for key in request.form.keys():
				all_list=(request.form.getlist(key))
				for each_list,each_file in zip(all_list,uploaded_files):
					modified_list=json.loads(each_list)
					int_list=list(modified_list.values())
					each_file.save(os.path.join(imagePath,each_file.filename))
					file_id=insert_ToDrive(each_file.filename,imagePath,folder_id)
					initcheck_id=int_list[0]
					damagedPart=int_list[1]
					damageType=int_list[2]
					initial_image=Init_Checklist_Images(initcheck_id,each_file.filename,file_id,damagedPart,damageType)
					db.session.add(initial_image)
			db.session.commit()
			file_status=True
	except:
		return 'Something went wrong',500
	else:
		if(file_status):
			return initChecklistImage_schema.jsonify(initial_image)
		else:
			return jsonify('Nothing')

		

@initialimage_route.route('/initialchecklist/image/update/<id>/',methods=['PUT'])
def update_customer(id):
	initial_image=Init_Checklist_Images.query.get(id)
	
	imageName=request.json['image_name']
	damagedPart=request.json['damaged_part']
	damageType=request.json['damage_type']

	initial_image.name=name
	initial_image.frame_id=frame_id
	initial_image.car_type=car_type
	initial_image.car_number=car_number

	db.session.commit()
	return initChecklistImage_schema.jsonify(initial_image)

@initialimage_route.route('/initialchecklist/image/delete/<id>/',methods=['DELETE'])
def delete_user(id):
	initial_image=Init_Checklist_Images.query.get(id)

	db.session.delete(initial_image)
	db.session.commit()

	return initChecklistImage_schema.jsonify(initial_image)
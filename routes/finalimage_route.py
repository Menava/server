from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,ma
import os
import json
from ..models.final_checklist import Final_Checklists,finalChecklist_schema,finalChecklists_schema
from ..models.final_checklist_image import Final_Checklist_Images,finalChecklistImage_schema,finalChecklistImages_schema

from ..config import imagePath,final_imageFolder
from .googleService_route import insert_ToDrive,delete_fileDrive

finalImage_route=Blueprint('finalImage_route',__name__)

folder_id=final_imageFolder

@finalImage_route.route('/finalchecklist/image/get',methods=['GET'])
def get_finalImages():
	all_finalImages=Final_Checklist_Images.query.all()
	results=finalChecklistImages_schema.dump(all_finalImages)
	return jsonify(results)


@finalImage_route.route('/finalchecklist/image/get/<id>/',methods=['GET'])
def post_details(id):
	final_images=Final_Checklist_Images.query.filter(Final_Checklist_Images.finalChecklist_id==id).all()
	return finalChecklistImages_schema.jsonify(final_images)

@finalImage_route.route('/finalchecklist/image/upload/',methods=['POST'])
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
					final_images=Final_Checklist_Images(initcheck_id,each_file.filename,file_id,damagedPart,damageType)
					db.session.add(final_images)
			db.session.commit()
			file_status=True
	
	except Exception as e:
		print(e)
		return 'Something went wrong',500
	
	else:
		if(file_status):
			return finalChecklistImage_schema.jsonify(final_images)
		else:
			return jsonify('Nothing')

@finalImage_route.route('/finalchecklist/image/update/<id>/',methods=['PUT'])
def update_finalImage(id):
	final_images=Final_Checklist_Images.query.get(id)
	
	imageName=request.json['image_name']
	damagedPart=request.json['damaged_part']
	damageType=request.json['damage_type']

	final_images.name=name
	final_images.frame_id=frame_id
	final_images.car_type=car_type
	final_images.car_number=car_number

	db.session.commit()
	return finalChecklistImage_schema.jsonify(final_images)

@finalImage_route.route('/finalchecklist/image/delete/<id>/',methods=['DELETE'])
def delete_finalImage(id):
	final_images=Final_Checklist_Images.query.get(id)

	db.session.delete(final_images)
	db.session.commit()

	return finalChecklistImage_schema.jsonify(final_images)
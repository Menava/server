from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db
import os
from ..models.supplier import Suppliers,supplier_schema,suppliers_schema
from ..models.item import Items,item_schema,items_schema

from ..config import imagePath,item_folder
from .googleService_route import insert_ToDrive,delete_fileDrive


item_route=Blueprint('item_route',__name__)

folder_id=item_folder

@item_route.route('/item/get',methods=['GET'])
def get_items():
	item_array=[]
	items = db.session.query(Items, Suppliers).filter(Items.hidden==False).join(Suppliers).all()
	for item, supplier in items:
		item_result=item_schema.dump(item)
		supplier_result=supplier_schema.dump(supplier)
		item_result["supplier_id"]=supplier_result
		item_result["supplier"]=item_result["supplier_id"]
		del item_result["supplier_id"]
		item_array.append(item_result)
		

	return jsonify(item_array)


@item_route.route('/item/get/<id>/',methods=['GET'])
def post_details(id):
	item=Items.query.get(id)
	return item_schema.jsonify(item)


@item_route.route('/item/add/',methods=['POST'])
def add_item():
	# try:
	# 	files=request.files
	# 	image = files.get('file')
	# 	name=request.form.get('name')
	# 	quantity=request.form.get('quantity')
	# 	price=request.form.get('price')
	# 	refundable=request.form.get('refundable')
	# 	supplier_id=request.form.get('supplier_id')
	# 	image.save(os.path.join(imagePath,image.filename))

	# 	file_id=insert_ToDrive(image.filename,imagePath,folder_id)

	# 	if refundable=='true':
	# 		refundable=True
	# 	else:
	# 		refundable=False

	# 	item=Items(name,quantity,price,image.filename,file_id,refundable,supplier_id)
	# 	db.session.add(item)
	# 	db.session.commit()
	# except Exception as e:
	# 	print(e)
	# 	return 'something went wrong',500
	# else:
	# 	return item_schema.jsonify(item)

	files=request.files
	image = files.get('file')
	name=request.form.get('name')
	quantity=request.form.get('quantity')
	price=request.form.get('price')
	refundable=request.form.get('refundable')
	supplier_id=request.form.get('supplier_id')
	image.save(os.path.join(imagePath,image.filename))

	file_id=insert_ToDrive(image.filename,imagePath,folder_id)

	if refundable=='true':
		refundable=True
	else:
		refundable=False

	item=Items(name,quantity,price,image.filename,file_id,refundable,supplier_id)
	db.session.add(item)
	db.session.commit()

	return item_schema.jsonify(item)
	
@item_route.route('/item/update/<id>/',methods=['PUT'])
def update_item(id):
	item=Items.query.get(id)

	try:
		files=request.files
		if files:
			# os.remove(os.path.join(imagePath, item.item_imageName))
			delete_fileDrive(item.item_imagePath)
			image = files.get('file')
			image.save(os.path.join(imagePath,image.filename))
			file_id=insert_ToDrive(image.filename,imagePath,folder_id)
			item.item_imageName=image.filename
			item.item_imagePath=file_id
		else:
			image=request.form.get('file')
			item.item_imageName=item.item_imageName
		
		name=request.form.get('name')
		quantity=request.form.get('quantity')
		price=request.form.get('price')
		supplier_id=request.form.get('supplier_id')
		refundable=request.form.get('refundable')

		item.name=name
		item.quantity=quantity
		item.price=price
		item.supplier_id=supplier_id

		db.session.commit()
	except:
		return 'Something went wrong',500
	else:
		return item_schema.jsonify(item)

@item_route.route('/item/delete/<id>/',methods=['PUT'])
def delete_item(id):
	item=Items.query.get(id)

	item.hidden=True
	db.session.commit()

	return item_schema.jsonify(item)
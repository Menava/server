from flask import jsonify, request, Blueprint,session
from ..extensions import db,ma
from ..Google import google_service
from flask_sqlalchemy import SQLAlchemy

from ..models.employee import Employees,employee_schema,employees_schema

from ..models.item import Items,item_schema,items_schema

from ..routes.notification_route import check_notications

import json
# from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,current_user,get_jwt

# from flask_socketio import emit,send


app_route = Blueprint('app_route', __name__)
clients=0
item_array=[]

# # Socket IO
# @socketio.on('item_event')
# def handle_my_custom_event(json):
#     global last_emitData
#     print(json)
#     print("item_event")
#     last_emitData=json
#     emit("receive_items",json,broadcast=True)

# def ack():
#     print('message was received!')

# @socketio.on("connect")
# def test_connect():
#     global clients
#     clients+=1
#     print("Client ID:",request.sid,"has connected.Current clients:",clients)
#     emit('user-connected', clients, broadcast=True, include_self=False)

# @socketio.on('disconnect')
# def test_disconnect():
#     global clients
#     global last_emitData
#     clients-=1
#     print("last emit data",last_emitData)
#     print("Client ID:",request.sid,"has disconnected.Current clients:",clients)
#     emit("disconnect",last_emitData,broadcast=True)

# #Item Management
# @app_route.route('/init_itemArray/get',methods=['GET'])
# def init_itemsArray():
#     global item_array
#     items = db.session.query(Items).all()
#     item_array=items_schema.dump(items)

#     print(item_array)
#     return jsonify(item_array)

# @app_route.route('/init_itemArray/edit/<option>',methods=['POST'])
# def edit_itemsArray(option):
#     user_items=json.loads(request.form.get('user-items'))
#     global item_array

#     for i in range(len(item_array)):
#         print(item_array[i]["id"])
#         # if(user_items["item id"]==i["id"]):
#         #     if(option=='positive'):
#         #         pass
#         #     else:
#         #         print("negative")
#     return jsonify(item_array)


# #Session
# @app_route.route('/set-session/<value>')
# def set_session(value):
#     session['value']=value
#     return 'test'

# @app_route.route('/get-session/')
# def get_session():
#     return jsonify(user=session.get("user"),
#     value=session.get('value'),
#     user_items=session.get('user-items'))

# @app_route.route('/delete-session/')
# def delete_session():
#     session.clear()
#     return 'session has been clear'

# @app_route.route('/set-userItems/',methods=['POST'])
# def add_userItem():
#     user_items=request.form.get('user-items')

#     session['user-items']=json.loads(user_items)

#     return jsonify(session['user-items'])

# @app_route.route('/append-userItems/',methods=['POST'])
# def append_userItem():
#     item_inList=False
#     user_items=request.form.get('user-items')
#     unloaded_data=json.loads(user_items)

#     for i in session["user-items"]:
#         if(unloaded_data["item id"]==i["item id"]):
#             print("true")
#             i["quantity"]+=unloaded_data["quantity"]
#             item_inList=True
#     if(item_inList==False):
#         session["user-items"].append(unloaded_data)

#     return jsonify(session['user-items'])

@app_route.route('/login/<username>/<password>')
def login(username,password):
    employee = Employees.query.filter_by(username=username).one_or_none()

    if not employee or employee.password!=password:
        return jsonify("404")
    # session["user"]=employee_schema.dump(employee)
    # session['user-items']=[]

    check_notications()
    return jsonify(employee_schema.dump(employee))

# @app_route.route('/logout')
# def logout():
#     session.clear()
#     return 'user has been logout'

#Notification


#Database
@app_route.route("/reset/<option>", methods=["GET"])
def reset_database(option):
    db.drop_all()
    db.create_all()
    file=open(r"server\others\sample_data")
    sql = file.read()
    if(option=="withdata"):
        db.engine.execute(sql)
    
    return "reset"

#JWT
#   
# def user_identity_lookup(employee):
#     print(employee)
#     return employee.id

# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     return Employees.query.filter_by(id=identity).one_or_none() 

# #Routes
# @app_route.route('/login', methods=['POST'])
# def login():
#     username = request.json.get("username")
#     password = request.json.get("password")

#     employee = Employees.query.filter_by(username=username).one_or_none()

#     # if not employee or not employees.check_password(password):
#     #     return jsonify("Wrong username or password"), 401
#     additional_claims = {"aud": "some_audience", "foo": "bar"}
#     access_token = create_access_token(identity=employee,additional_claims=additional_claims)
#     print(access_token)
#     return jsonify(access_token=access_token)

# @app_route.route('/logout', methods=['POST'])
# def logout():
#     pass

# @app_route.route("/get-claims", methods=["GET"])
# @jwt_required()
# def get_addClaims():
#     claims = get_jwt()
#     print(get_jwt())
#     return jsonify(foo=claims["foo"])


# @app_route.route("/current-user", methods=["GET"])
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     return jsonify(
#         id=current_user.id,
#         name=current_user.name,
#         username=current_user.username,
#         position=current_user.position,
#     )
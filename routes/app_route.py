from flask import jsonify, request, Blueprint,session
from ..extensions import db,ma

from flask_sqlalchemy import SQLAlchemy

from ..models.employee import Employees,employee_schema,employees_schema

from ..models.item import Items,item_schema,items_schema

from ..routes.notification_route import check_notications

import json

app_route = Blueprint('app_route', __name__)

@app_route.route('/login/<username>/<password>')
def login(username,password):
    print("log in in")
    employee = Employees.query.filter_by(username=username).one_or_none()

    if not employee or employee.password!=password:
        return jsonify("404")
    # session["user"]=employee_schema.dump(employee)
    # session['user-items']=[]

    check_notications()
    return jsonify(employee_schema.dump(employee))

#Database
@app_route.route("/reset/<option>", methods=["GET"])
def reset_database(option):
    sql_command = ''
    db.drop_all()
    db.create_all()
    if(option=="withdata"):
        print('here')
        sql_file=open(r"/home/genshinimpact1234/mysite/server/others/sql.text",'r')
        for line in sql_file:
            if not line.startswith('--') and line.strip('\n'):
                sql_command += line.strip('\n')
                if sql_command.endswith(';'):
                    try:
                        db.session.execute(sql_command)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                    finally:
                        sql_command = ''
    return "reset"
from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,getTargetDate
import os

from ..models.item import Items,item_schema,items_schema
from ..models.customer import Customers,customer_schema,customers_schema
from ..models.notification import Notifications,notification_schema,notifications_schema
from ..models.voucher import Vouchers,voucher_schema,vouchers_schema
from ..models.service_item import Services_items,serviceItem_schema,serviceItems_schema
from ..models.customer_item import Customer_items,customerItem_schema,customerItems_schema
from ..models.service import Services,service_schema,services_schema
from ..models.customer_car import Customers_cars,customerCar_schema,customerCars_schema
from ..models.voucher_serviceitem import Vouchers_servicesitems,voucherServiceItem_schema,voucherServiceItems_schema

notification_route=Blueprint('notification_route',__name__)
targetMonth=6
targetDay=2

@notification_route.route('/notification/get',methods=['GET'])
def get_notifications():
    all_notis=Notifications.query.all()
    results=notifications_schema.dump(all_notis)
    return jsonify(results)

@notification_route.route('/notification/update/<id>', methods=['PUT'])
def update_notification(id):
    noti = Notifications.query.get(id)
    noti.seen=True
    db.session.commit()

    return jsonify(notification_schema.dump(noti))

@notification_route.route('/notification/delete/<id>/',methods=['PUT'])
def delete_notifications(id):
    pass

def check_notications():
    customer_notis=check_customerNoti()
    if customer_notis:
        for customer_noti in customer_notis:
            checkNoti=Notifications.query.filter(Notifications.description==customer_noti.description).first()
            if not checkNoti:
                db.session.add(customer_noti)
        db.session.commit()

def check_customerNoti():
    noti_array=[]
    target_date1=getTargetDate(targetMonth)
    target_date2=getTargetDate(targetMonth,targetDay)
    results = db.session.query(Vouchers,Vouchers_servicesitems,Customers_cars).join(Vouchers_servicesitems,Services_items,Customers_cars).filter(Services_items.service_id==2,Vouchers.date<=target_date1,Vouchers.date>=target_date2).all()
    if results:
        for voucher,voucher_service,customer_car in results:
            voucher_service_result=db.session.query(Services).join(Services_items,Vouchers_servicesitems).filter(Vouchers_servicesitems.id==voucher_service.id).first()
            customer_results=db.session.query(Customers).join(Customers_cars).filter(Customers_cars.id==customer_car.id).first()
            customer_detail=customer_schema.dump(customer_results)
            service_detail=service_schema.dump(voucher_service_result)
            description='{name} has performed {service} {month} months ago'.format(name=customer_detail["name"],service=service_detail["service_type"],month=targetMonth)
            notification=Notifications(customer_detail["id"],None,description)
            noti_array.append(notification)
    return noti_array

def check_itemNoti():
    pass

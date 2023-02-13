from flask import jsonify,request,render_template,redirect,Blueprint
from ..extensions import db,getTodayDate

from ..models.item_purchase import Items_Purchase,itemPurchase_schema,itemPurchases_schema
from ..models.item import Items,item_schema,items_schema
from ..models.item_payment import Items_Payment,itemPayment_schema,itemPayments_schema
from datetime import date

itempurchases_route=Blueprint('itempurchases_route',__name__)

@itempurchases_route.route('/item_purchase/get',methods=['GET'])
def get_itemPurchases():
    itemPurchase_array=[]
    all_itemPurchase=db.session.query(Items_Purchase,Items,Items_Payment).join(Items,Items_Payment).all()
    for item_purchase,item,item_payment in all_itemPurchase:
        itemPurchase_result=itemPurchase_schema.dump(item_purchase)
        item_result=item_schema.dump(item)
        itemPayment_result=itemPayment_schema.dump(item_payment)
        itemPurchase_result["item_id"]=item_result
        itemPurchase_result["item_payment"]=itemPayment_result
        itemPurchase_array.append(itemPurchase_result)
    return jsonify(itemPurchase_array)

@itempurchases_route.route('/item_purchase/get/<id>/',methods=['GET'])
def get_itemPurchase(id):
    pass

@itempurchases_route.route('/item_purchase/add/',methods=['POST'])
def add_itemPurchase():
    print("----------------------------------------")
    quantity_received=int(request.json['quantity_received'])
    refund_quantity=request.json['refund_quantity']
    unit_price=request.json['unit_price']
    sell_price=request.json['sell_price']
    item_id=request.json['item_id']
    status=request.json["status"]

    valueExist=False

    itemPurchase=checkItemPurchase(item_id)
    if(itemPurchase!=None):
        original_quantity=quantity_received
        item=getRefundQty(item_id,quantity_received,unit_price)
        quantity_beforeChange=item.quantity
        if(item.refundable!=False):
            quantity_received+=item.quantity
            valueExist=True
        item.quantity+=original_quantity
        item.price=sell_price

    itemPurchase=Items_Purchase(quantity_received,refund_quantity,unit_price,item_id,status)
    db.session.add(itemPurchase)
    if(valueExist==True):
        refresh_itemRelatedValues(item_id,original_quantity,unit_price,item,quantity_beforeChange)
    db.session.commit()
    
    return itemPurchase_schema.jsonify(itemPurchase)

@itempurchases_route.route('/item_purchase/update/<id>/',methods=['PUT'])
def update_itemPurchase(id):
    item_purchase=Items_Purchase.query.filter(Items_Purchase.item_id==id,Items_Purchase.status==False).order_by(Items_Purchase.id.desc()).first()
    refund_quantity=int(request.json['refundQty'])

    item_purchase.refund_quantity+=refund_quantity
    amount=calculate_total(item_purchase.refund_quantity,item_purchase.quantity_received,item_purchase.unit_price)

    item_payment=Items_Payment.query.filter(Items_Payment.purchase_id==item_purchase.id).first()
    item_payment.paid_amount=amount

    item=Items.query.filter(Items.id==item_purchase.item_id).first()
    item.quantity-=refund_quantity

    db.session.commit()

    return itemPurchase_schema.jsonify(item_purchase)

@itempurchases_route.route('/item_purchase/delete/<id>/',methods=['DELETE'])
def delete_itemPurchase(id):
    pass

def refresh_itemRelatedValues(item_id,quantity_received,unit_price,item,quantity_beforeChange):
    itemPurchase=checkItemPurchase(item_id)
    # print(itemPurchase_schema.dump(itemPurchase))
    if(itemPurchase==None):
        return 
    else:
        itemPayment=Items_Payment.query.filter(Items_Payment.purchase_id==itemPurchase.id).order_by(Items_Payment.id.desc()).first()

        # print(itemPayment_schema.dump(itemPayment))

        itemPurchase.status=True
        itemPurchase.refund_quantity+=quantity_beforeChange

        new_paidAmount=calculate_total(itemPurchase.refund_quantity,itemPurchase.quantity_received,itemPurchase.unit_price)

        itemPayment.paid_amount=new_paidAmount
        
        db.session.commit()

def calculate_total(refund_quantity,quantity_received,unit_price):
    new_quantity=quantity_received-refund_quantity
    new_total=new_quantity*unit_price
    return new_total

def getRefundQty(item_id,quantity_received,unit_price):
    item=Items.query.filter(Items.id==item_id).first()
    return item

def checkItemPurchase(item_id):
    try:
        querys=Items_Purchase.query.all() 
        itemPurchase=Items_Purchase.query.filter(Items_Purchase.item_id==item_id).order_by(Items_Purchase.id.desc()).limit(2)[1] 
    except:
        querys=Items_Purchase.query.all() 
        itemPurchase=Items_Purchase.query.filter(Items_Purchase.item_id==item_id).order_by(Items_Purchase.id.desc()).first()
    return itemPurchase

def get_PurchaseDate(e):
    return e['purchase_date']

@itempurchases_route.route('/item_purchase/test/<id>',methods=['GET'])
def getItemPurchase(id):
    itm_qty=0
    result=db.session.query(Items_Purchase,Items).filter(Items_Purchase.item_id==id).join(Items).order_by(Items_Purchase.id.desc()).limit(2)
    for i in result:
        print(i)
    # itm_qty=result[0].quantity_received-result[1].refund_quantity
    # print('itm qty',itm_qty)

    return 'test'


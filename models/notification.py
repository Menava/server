from server import db,ma
from ..extensions import db,ma

class Notifications(db.Model):
    __tablename__ = 'notification'
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customers.id'),nullable=True)
    item_id=db.Column(db.Integer,db.ForeignKey('items.id'),nullable=True)
    description=db.Column(db.String(100))
    seen=db.Column(db.Boolean,default=False)

    def __init__(self,customer_id,item_id,description):
        self.customer_id=customer_id
        self.item_id=item_id
        self.description=description

class NotificationSchema(ma.Schema):
    class Meta:
        fields=('id','customer_id','item_id','description','seen')

notification_schema=NotificationSchema()
notifications_schema=NotificationSchema(many=True)
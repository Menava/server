from server import db,ma
from ..extensions import db,ma

class DamageTypes(db.Model):
    __tablename__ = 'damagetype'
    id=db.Column(db.Integer,primary_key=True)
    code=db.Column(db.String(100))
    description=db.Column(db.String(100))


    def __init__(self,code,description):
        self.code=code
        self.description=description


class DamageTypeSchema(ma.Schema):
    class Meta:
        fields=('id','name','description')

damageType_schema=DamageTypeSchema()
damageTypes_schema=DamageTypeSchema(many=True)
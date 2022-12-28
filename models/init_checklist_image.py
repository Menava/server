from server import db,ma
from ..extensions import db,ma

class Init_Checklist_Images(db.Model):
    __tablename__ = 'initimage'
    id=db.Column(db.Integer,primary_key=True)
    intChecklist_id=db.Column(db.Integer,db.ForeignKey('init_checklist.id'))
    imageName=db.Column(db.String(100))
    imagePath=db.Column(db.String(100))
    damagedPart=db.Column(db.String(100))
    damageType=db.Column(db.String(100))
    

    def __init__(self,intChecklist_id,imageName,imagePath,damagedPart,damageType):
        self.intChecklist_id=intChecklist_id
        self.imageName=imageName
        self.imagePath=imagePath
        self.damagedPart=damagedPart
        self.damageType=damageType

class InitChecklistImage_Schema(ma.Schema):
    class Meta:
        fields=('id','intChecklist_id','imageName','imagePath','damagedPart','damageType')

initChecklistImage_schema=InitChecklistImage_Schema()
initChecklistImages_schema=InitChecklistImage_Schema(many=True)
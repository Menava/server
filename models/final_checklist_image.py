from server import db,ma
from ..extensions import db,ma

class Final_Checklist_Images(db.Model):
    __tablename__='finalimage'
    id=db.Column(db.Integer,primary_key=True)
    finalChecklist_id=db.Column(db.Integer,db.ForeignKey('final_checklist.id'))
    imageName=db.Column(db.String(100))
    imagePath=db.Column(db.String(100))
    damagedPart=db.Column(db.String(100))
    damageType=db.Column(db.String(100))
    

    def __init__(self,finalChecklist_id,imageName,imagePath,damagedPart,damageType):
        self.finalChecklist_id=finalChecklist_id
        self.imageName=imageName
        self.imagePath=imagePath
        self.damagedPart=damagedPart
        self.damageType=damageType

class FinalChecklistImage_Schema(ma.Schema):
    class Meta:
        fields=('id','finalChecklist_id','imageName','imagePath','damagedPart','damageType')

finalChecklistImage_schema=FinalChecklistImage_Schema()
finalChecklistImages_schema=FinalChecklistImage_Schema(many=True)
from server import db,ma
from ..extensions import db,ma

class Frame_Components(db.Model):
    __tablename__ = 'frame_components'
    id=db.Column(db.Integer,primary_key=True)
    frame_id=db.Column(db.Integer,db.ForeignKey('car_frame.id'))
    component=db.Column(db.String(100))
    
    def __init__(self,frame_id,component):
        self.frame_id=frame_id
        self.component=component

class FrameComponents_Schema(ma.Schema):
    class Meta:
        fields=('id','frame_id','component')

frameComponent_schema=FrameComponents_Schema()
frameComponents_schema=FrameComponents_Schema(many=True)
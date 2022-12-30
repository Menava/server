from ..extensions import db,ma

class Google_cred(db.Model):
    __tablename__ = 'google_cred'
    id=db.Column(db.Integer,primary_key=True)
    cred=db.Column(db.String(100))
    state=db.Column(db.String(100))

    def __init__(self,cred=None,state=None):
        self.cred=cred
        self.state=state
    
    def add_cred(cred,state=None):
        google_cred = db.session.query(Google_cred).one()

        if(google_cred==None):
            google_cred=Google_cred(temp_cred,temp_state)
            db.session.add(google_cred)
	        
        else:
            google_cred.cred=cred
            google_cred.state=state
        db.session.commit()
    
    def get_cred():
        google_cred = db.session.query(Google_cred).one()
        return google_cred

class GoogleCredSchema(ma.Schema):
    class Meta:
        fields=('id','cred','state')

googleCred_schema=GoogleCredSchema()
googleCreds_schema=GoogleCredSchema(many=True)
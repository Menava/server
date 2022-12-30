from ..extensions import db,ma

class Google_cred(db.Model):
    __tablename__ = 'google_cred'
    id=db.Column(db.Integer,primary_key=True)
    token=db.Column(db.String(100))
    refresh_token=db.Column(db.String(100))
    token_uri=db.Column(db.String(100))
    client_id=db.Column(db.String(100))
    client_secret=db.Column(db.String(100))
    scopes=db.Column(db.String(100))

    def __init__(self,token=None,refresh_token=None,token_uri=None,client_id=None,client_secret=None,scopes=None):
        self.token=token
        self.refresh_token=refresh_token
        self.token_uri=token_uri
        self.client_id=client_id
        self.client_secret=client_secret
        self.scopes=scopes
    
    @staticmethod
    def add_cred(token=None,refresh_token=None,token_uri=None,client_id=None,client_secret=None,scopes=None):
        google_cred = db.session.query(Google_cred).first()

        if(google_cred==None):
            google_cred=Google_cred(token,refresh_token,token_uri,client_id,client_secret,scopes)
            db.session.add(google_cred)
	        
        else:
            google_cred.token=token
            google_cred.refresh_token=refresh_token
            google_cred.token_uri=token_uri
            google_cred.client_id=client_id
            google_cred.client_secret=client_secret
            google_cred.scopes=scopes
        db.session.commit()
    
    @staticmethod
    def get_cred():
        google_cred = db.session.query(Google_cred).first()
        if(google_cred!=None):
            schemeResult=googleCred_schema.dump(google_cred)
            del schemeResult["id"]
        return schemeResult

class GoogleCredSchema(ma.Schema):
    class Meta:
        fields=('id','token','refresh_token','token_uri','client_id','client_secret','scopes')

googleCred_schema=GoogleCredSchema()
googleCreds_schema=GoogleCredSchema(many=True)
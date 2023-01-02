from ..extensions import db,ma

class Google_cred(db.Model):
    __tablename__ = 'google_cred'
    id=db.Column(db.Integer,primary_key=True)
    token=db.Column(db.String(1000))
    refresh_token=db.Column(db.String(1000))
    token_uri=db.Column(db.String(300))
    client_id=db.Column(db.String(300))
    client_secret=db.Column(db.String(300))
    scopes=db.Column(db.String(300))

    def __init__(self,token=None,refresh_token=None,token_uri=None,client_id=None,client_secret=None,scopes=None):
        self.token=token
        self.refresh_token=refresh_token
        self.token_uri=token_uri
        self.client_id=client_id
        self.client_secret=client_secret
        self.scopes=scopes
    
    @staticmethod
    def add_cred(token=None,refresh_token=None,token_uri=None,client_id=None,client_secret=None,scopes=None):
        modified_scope=scopes[0]

        google_cred = db.session.query(Google_cred).first()
        print("add cred in ",google_cred)
        if(google_cred==None):
            print("if in")
            google_cred=Google_cred(token,refresh_token,token_uri,client_id,client_secret,modified_scope)
            db.session.add(google_cred)
	        
        else:
            print("else in")
            google_cred.token=token
            # google_cred.refresh_token=refresh_token
        print("google_cred in add",googleCred_schema.dump(google_cred))
        db.session.commit()
    
    @staticmethod
    def get_cred():
        schemeResult=None
        google_cred = Google_cred.query.first()
        
        if(google_cred!=None):
            new_scope=[google_cred.scopes]
            google_cred.scopes=new_scope
            schemeResult=googleCred_schema.dump(google_cred)
            del schemeResult["id"]
        db.session.delete(google_cred)
        return schemeResult

class GoogleCredSchema(ma.Schema):
    class Meta:
        fields=('id','token','refresh_token','token_uri','client_id','client_secret','scopes')

googleCred_schema=GoogleCredSchema()
googleCreds_schema=GoogleCredSchema(many=True)
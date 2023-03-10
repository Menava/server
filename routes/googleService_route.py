from flask import jsonify, request, Blueprint,session
from ..extensions import db,ma

from googleapiclient.http import MediaFileUpload
import os,shutil

from ..config import imagePath
from ..Google import load_googleService

googleService_route = Blueprint('googleService_route', __name__)


folder_id='1b0z1BZrVuP2N-47_LD9uj_A37b-aCNOe'

@googleService_route.route('/drive/createfolder/<value>')
def create_folder(value):
    google_service=load_googleService()
    file_metadata={
        'name':value,
        'mimeType':'application/vnd.google-apps.folder',
        'parents':[]
    }
    google_service.files().create(body=file_metadata).execute()

    return 'Test'

@googleService_route.route('/drive/image/add',methods=['POST'])
def add_image():
    google_service=load_googleService()
    files=request.files
    image = files.get('image_form')
    image.save(os.path.join(imagePath,image.filename))

    file_name=image.filename
    
    file_metadata={
        'name':file_name,
        'parents':[folder_id]        
    }
    media=MediaFileUpload(os.path.join(imagePath,image.filename),mimetype='image/jpeg')

    file_id=google_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return 'test'

def insert_ToDrive(file_name,imagePath,folder_id):
    google_service=load_googleService()
    print("service google",google_service)
    file_metadata={
        'name':file_name,
        'parents':[folder_id]        
    }
    media=MediaFileUpload(os.path.join(imagePath,file_name),mimetype='image/jpeg')

    file_id=google_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print('file_id',file_id)
    print("here 1")
    print('file_id id',file_id["id"])
    return file_id["id"]

def delete_fileDrive(file_id):
    google_service=load_googleService()
    google_service.files().delete(fileId=file_id).execute()

@googleService_route.route('/drive/clearfolder')
def clear_images():   
    for filename in os.listdir(imagePath):
        file_path = os.path.join(imagePath, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return 'test'
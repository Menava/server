import pickle,google_auth_oauthlib,os.path,os,flask,json,requests
from flask import jsonify, request,session,Blueprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow,InstalledAppFlow
from googleapiclient.discovery import build

from .config import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,SCOPE,API_NAME,API_VERSION,CLIENT_SECRET_FILE

temp_cred=None
temp_state=None
google_service=None
google_route = Blueprint('google_route', __name__)

# @google_route.route('/create_service')
# def create_service():
#     cred = None

#     pickle_file = f'token_{API_NAME}_{API_VERSION}.pickle'
#     # print(pickle_file)

#     if os.path.exists(pickle_file):
#         with open(pickle_file, 'rb') as token:
#             cred = pickle.load(token)

#     if not cred or not cred.valid:
#         if cred and cred.expired and cred.refresh_token:
#             cred.refresh(Request())
#         else:
#             return flask.redirect('authorize')

#         with open(pickle_file, 'wb') as token:
#             pickle.dump(cred, token)

#     try:
#         cred = google.oauth2.credentials.Credentials(
#       **flask.session['credentials'])
#         service = build(API_NAME, API_VERSION, credentials=cred)
#         google_service=service
#     except Exception as e:
#         print('Unable to connect.')
#         print(e)

# @google_route.route('/authorize')
# def authorize():
#   flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#       CLIENT_SECRET_FILE, scopes=SCOPE)

#   flow.redirect_uri = flask.url_for('google_route.oauth2callback', _external=True)

#   authorization_url = auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
#                 '&client_id={}&redirect_uri={}&scope={}').format(CLIENT_ID, REDIRECT_URI, SCOPE)
#   return flask.redirect(authorization_url)


# @google_route.route('/oauth2callback')
# def oauth2callback():

#   flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#       CLIENT_SECRET_FILE, scopes=SCOPE)

#   flow.redirect_uri = flask.url_for('google_route.oauth2callback', _external=True)

#   authorization_response = flask.request.url
#   flow.fetch_token(authorization_response=authorization_response)

#   credentials = flow.credentials
#   flask.session['credentials'] = credentials_to_dict(credentials)
#   return flask.redirect(flask.url_for('google_route.create_service'))

# def credentials_to_dict(credentials):
#   return {'token': credentials.token,
#           'refresh_token': credentials.refresh_token,
#           'token_uri': credentials.token_uri,
#           'client_id': credentials.client_id,
#           'client_secret': credentials.client_secret,
#           'scopes': credentials.scopes}

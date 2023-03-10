import pickle,google_auth_oauthlib,os.path,os,flask,json,requests
from flask import jsonify, request,session,Blueprint,redirect,url_for
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow,InstalledAppFlow
from googleapiclient.discovery import build

from .models.google_cred import Google_cred,googleCred_schema

from .config import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,SCOPE,API_NAME,API_VERSION,CLIENT_SECRET_FILE

google_route = Blueprint('google_route', __name__)
temp_state=None
googleCred=Google_cred()

@google_route.route('/getCred')
def getCredd():
  google_cred=googleCred.get_cred()
  print("Get cred",google_cred)
  return jsonify('test')

def load_googleService():
  print("load in")
  service=None
  google_cred=googleCred.get_cred()
  print('google_cred',google_cred)
  if google_cred!=None:
    credentials=Credentials(**google_cred)
    googleCred.add_cred(credentials.token,credentials.refresh_token,credentials.token_uri,credentials.client_id,credentials.client_secret,credentials.scopes)
  else:
    return redirect('authorize')
  service = build(API_NAME, API_VERSION, credentials=credentials)
  

  return service

@google_route.route('/')
def create_service():
  print("create in")  
  google_cred=googleCred.get_cred()

  if google_cred==None:
    return redirect('authorize')
  
  return jsonify("Google authentication success")

@google_route.route('/authorize')
def authorize():
  global temp_state
  print("auth in")
  flow = Flow.from_client_secrets_file(
      CLIENT_SECRET_FILE, scopes=SCOPE)

  flow.redirect_uri = url_for('google_route.oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true')
  temp_state=state

  return redirect(authorization_url)


@google_route.route('/oauth2callback')
def oauth2callback():
  global temp_state
  print("oauth in")
  flow = Flow.from_client_secrets_file(
      CLIENT_SECRET_FILE, scopes=SCOPE,state=temp_state)

  flow.redirect_uri = url_for('google_route.oauth2callback', _external=True)

  authorization_response = request.url
  flow.fetch_token(authorization_response=authorization_response)

  credentials = flow.credentials
  print('credentials',credentials.token)
  print("credentials in auth",credentials_to_dict(credentials))
  googleCred.add_cred(credentials.token,credentials.refresh_token,credentials.token_uri,credentials.client_id,credentials.client_secret,credentials.scopes)

  return flask.redirect(flask.url_for('google_route.create_service'))


@google_route.route('/revoke')
def revoke():
  google_cred=googleCred.get_cred()

  if google_cred==None:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = Credentials(
    **google_cred)

  revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.' + print_index_table())
  else:
    return('An error occurred.' + print_index_table())


@google_route.route('/clear')
def clear_credentials():
  if 'credentials' in flask.session:
    del flask.session['credentials']
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def print_index_table():
  return ('<table>' +
          '<tr><td><a href="/test">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')
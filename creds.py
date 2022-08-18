import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tokens.api_key import API_KEY

APP_TOKEN_FILE = "tokens/client_secret.json"
USER_TOKEN_FILE = "tokens/user_token.json"

SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/youtube.upload',
]

def get_creds_saved():
    creds = None

    if os.path.exists(USER_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(USER_TOKEN_FILE, SCOPES)
        creds.refresh(Request())

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

    with open(USER_TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

    return creds


def get_service_creds(service = 'youtube', version = 'v3'):
    creds = get_creds_saved()
    service = build(service, version, credentials=creds)
    return service


def get_service_simple(service = 'youtube', version = 'v3'):
    return  build(service, version, developerKey=API_KEY)
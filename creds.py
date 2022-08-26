from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube.upload',
]


def get_service_creds(user_token, service = 'youtube', version = 'v3'):
    creds = Credentials.from_authorized_user_file(user_token, SCOPES)

    if not creds.valid:
        creds.refresh(Request())

        with open(user_token, 'w') as token:
            token.write(creds.to_json())

    service = build(service, version, credentials=creds)
    return service


def get_service_simple(api_key, service = 'youtube', version = 'v3'):
    return  build(service, version, developerKey=api_key)
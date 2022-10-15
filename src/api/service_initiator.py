import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.common.variables import SCOPES


def init_services(api_name, api_version, delegated_user=None):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES[api_name])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES[api_name])
            creds = flow.run_local_server()

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    if delegated_user is not None:
        credentials = service_account.Credentials.from_service_account_file(
            'service.json', scopes=SCOPES[api_name])
        creds = credentials.with_subject(delegated_user)

    try:
        service = build(api_name, api_version, credentials=creds)
        return service
    except Exception as e:
        print(f'An error occurred: {e}')

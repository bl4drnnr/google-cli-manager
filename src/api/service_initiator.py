import os.path
import sys
import json
import httplib2
import google.oauth2.service_account
import google_auth_httplib2
import google.oauth2.id_token
import googleapiclient
import googleapiclient.discovery
import googleapiclient.errors

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.common.variables import SCOPES
from src.api.common.read_file import read_file


def get_api_version(api):
    if api == 'oauth2':
        return 'v2'
    elif api == 'gmail':
        return 'v1'
    elif api == 'groupsmigration':
        return 'v1'
    elif api == 'drive':
        return 'v2'
    return 'v1'


def get_service_acc_credentials(scopes, act_as):
    try:
        json_string = read_file(os.path.join(os.getcwd(), 'service.json'))
        if not json_string:
            print('There is no credentials file.')
            sys.exit()
        sa_info = json.loads(json_string)
        credentials = google.oauth2.service_account.Credentials.from_service_account_info(sa_info)
        credentials = credentials.with_scopes(scopes)
        credentials = credentials.with_subject(act_as)
        request = google_auth_httplib2.Request(_create_http_object())
        credentials.refresh(request)
        return credentials
    except (ValueError, KeyError):
        print('Wrong credential file.')
        sys.exit()


def _create_http_object(cache=None, timeout=600):
    http_args = {'cache': cache, 'timeout': timeout}
    return httplib2.Http(**http_args)


def init_services(api_name, api_version, delegated_user=None):
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
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

    service = build(api_name, api_version, credentials=creds)
    return service


def init_service_account_object(api, email, use_admin):
    auth_as = use_admin if use_admin else email
    scopes = SCOPES[api]
    credentials = get_service_acc_credentials(scopes, auth_as)
    httpc = _create_http_object()
    request = google_auth_httplib2.Request(httpc)
    credentials.refresh(request)
    version = get_api_version(api)
    try:
        service = googleapiclient.discovery.build(
            api,
            version,
            http=httpc,
            cache_discovery=False,
            static_discovery=False)
        service._http = google_auth_httplib2.AuthorizedHttp(credentials, http=httpc)
        return service
    except (httplib2.ServerNotFoundError, RuntimeError) as e:
        print(e)
        sys.exit()
    except google.auth.exceptions.RefreshError as e:
        if isinstance(e.args, tuple):
            e = e.args[0]
        print(e)
        sys.exit()


def init_group_service(delegated_user):
    credentials = service_account.Credentials.from_service_account_file(
        'service.json', scopes=['https://www.googleapis.com/auth/cloud-identity.groups'])
    delegated_credentials = credentials.with_subject(delegated_user)

    service_name = 'cloudidentity'
    api_version = 'v1'
    service = googleapiclient.discovery.build(
        service_name,
        api_version,
        credentials=delegated_credentials)

    return service

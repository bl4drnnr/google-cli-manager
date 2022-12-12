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


def _create_http_object(cache=None, timeout=600):
    http_args = {'cache': cache, 'timeout': timeout}
    return httplib2.Http(**http_args)


def _get_api_version(api):
    if api == 'oauth2':
        return 'v2'
    elif api == 'gmail':
        return 'v1'
    elif api == 'groupsmigration':
        return 'v1'
    elif api == 'drive':
        return 'v3'
    elif api == 'calendar':
        return 'v3'
    elif api == 'admin':
        return 'directory_v1'
    elif api == 'docs':
        return 'v1'
    elif api == 'iam':
        return 'v1'
    elif api == 'cloudidentity':
        return 'v1'
    return 'v1'


class ServiceInitiator:
    def __init__(self, api_name, delegated_user=None):
        self._api_name = api_name
        self._delegated_user = delegated_user

    def init_services(self):
        os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
        creds = None

        api_scope = SCOPES[self._api_name]
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', api_scope)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', api_scope)
                creds = flow.run_local_server()

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        if self._delegated_user is not None:
            credentials = service_account.Credentials.from_service_account_file(
                'service.json', scopes=api_scope)
            creds = credentials.with_subject(self._delegated_user)

        service = build(self._api_name, _get_api_version(self._api_name), credentials=creds)
        return service

    def init_service_account_object(self, email, use_admin):
        def get_service_acc_credentials(service_scopes, act_as):
            try:
                json_string = read_file(os.path.join(os.getcwd(), 'service.json'))
                if not json_string:
                    print('There is no credentials file.')
                    sys.exit()
                sa_info = json.loads(json_string)
                service_credentials = google.oauth2.service_account.Credentials.from_service_account_info(sa_info)
                service_credentials = service_credentials.with_scopes(service_scopes)
                service_credentials = service_credentials.with_subject(act_as)
                service_request = google_auth_httplib2.Request(_create_http_object())
                service_credentials.refresh(service_request)
                return service_credentials
            except (ValueError, KeyError):
                print('Wrong credential file.')
                sys.exit()

        auth_as = use_admin if use_admin else email
        scopes = SCOPES[self._api_name]
        credentials = get_service_acc_credentials(scopes, auth_as)
        httpc = _create_http_object()
        request = google_auth_httplib2.Request(httpc)
        credentials.refresh(request)
        version = _get_api_version(self._api_name)
        try:
            service = googleapiclient.discovery.build(
                self._api_name,
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

    def init_group_service(self):
        credentials = service_account.Credentials.from_service_account_file(
            'service.json', scopes=SCOPES[self._api_name])
        delegated_credentials = credentials.with_subject(self._delegated_user)

        service = googleapiclient.discovery.build(
            self._api_name,
            _get_api_version(self._api_name),
            credentials=delegated_credentials)

        return service

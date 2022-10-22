import os
import sys
import json
import base64

from src.common.print_text import print_text
from src.api.common.call_api import call_api
from src.api.service_initiator import init_services
from src.api.common.read_file import read_file

from src.common.variables import SCOPES


def get_service_account_client_id():
    try:
        json_string = read_file(os.path.join(os.getcwd(), 'service.json'))
        if not json_string:
            sys.exit()
        sa_info = json.loads(json_string)
        client_id = sa_info.get('client_id')
        if not client_id:
            sys.exit()
        return client_id
    except (ValueError, KeyError):
        sys.exit()


def set_project_consent_screen(stdscr=None):
    print_text(f'Checking service account DwD...', stdscr)
    all_scopes = []

    for item, value in SCOPES.items():
        for scope in value:
            all_scopes.append(scope)

    all_scopes.sort()
    client_id = get_service_account_client_id()
    long_url = ('https://admin.google.com/ac/owl/domainwidedelegation'
                f'?clientScopeToAdd={",".join(all_scopes)}'
                f'&clientIdToAdd={client_id}&overwriteClientId=true')
    print_text('\n\nPlease, go to this URL address, and click "Authorize":\n\n', stdscr)
    print_text(long_url, stdscr)
    print_text('\nThis is needed in order to allow you be able to manage data you want to manage.\n\n', stdscr)


def generate_service_account(project_id, admin_email, stdscr=None):
    try:
        print_text('Generating service account...', stdscr)
        service_account_file = os.path.join(os.getcwd(), 'service.json')
        iam = init_services('iam', 'v1', None)

        username = admin_email.split("@")[0]
        sa_body = {
            'accountId': username,
            'serviceAccount': {
                'displayName': f'{username} Service Account'
            }
        }
        service_account = call_api(iam.projects().serviceAccounts(), 'create',
                                   name='projects/%s' % project_id,
                                   body=sa_body, stdscr=stdscr)
        key_body = {
            'privateKeyType': 'TYPE_GOOGLE_CREDENTIALS_FILE',
            'keyAlgorithm': 'KEY_ALG_RSA_2048'
        }
        key = call_api(iam.projects().serviceAccounts().keys(), 'create',
                       name=service_account['name'], body=key_body, retry_reasons=[404])
        oauth2service_data = base64.b64decode(key['privateKeyData'])
        write_file(service_account_file, oauth2service_data)
        set_project_consent_screen(stdscr)
        print_text('Service account has been successfully created!', stdscr)

    except (Exception,):
        pass


def generate_credentials_file(client_id, client_secret, project_id, stdscr=None):
    print_text('Generating file with credentials...', stdscr)
    cs_data = '''{
        "installed": {
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "client_id": "%s",
            "client_secret": "%s",
            "project_id": "%s",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
            "token_uri": "https://accounts.google.com/o/oauth2/token"
        }
    }''' % (client_id, client_secret, project_id)
    client_secrets_file = 'credentials.json'
    write_file(client_secrets_file, cs_data, stdscr=stdscr)
    print_text('Credentials file has been successfully generated!', stdscr)


def write_file(filename, data, stdscr=None, mode='wb'):
    if isinstance(data, str):
        data = data.encode('utf-8')
    try:
        with open(os.path.expanduser(filename), mode) as f:
            f.write(data)
        return True
    except IOError as error:
        print_text(error, stdscr)

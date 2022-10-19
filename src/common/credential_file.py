import os
import base64

from src.common.print_text import print_text
from src.api.common.call_api import call_api
from src.api.service_initiator import init_service_account_object


def generate_service_account(project_id, admin_email, stdscr=None):
    print_text('Generating service account...', stdscr)
    service_account_file = os.path.join(os.getcwd(), 'service.json')
    iam = init_service_account_object('iam', None, admin_email)
    sa_body = {
        'accountId': project_id,
        'serviceAccount': {
            'displayName': f'{admin_email.split("@")[0]} Service Account'
        }
    }
    service_account = call_api(iam.projects().serviceAccounts(), 'create',
                               name='projects/%s' % project_id,
                               body=sa_body)
    key_body = {
        'privateKeyType': 'TYPE_GOOGLE_CREDENTIALS_FILE',
        'keyAlgorithm': 'KEY_ALG_RSA_2048'
    }
    key = call_api(iam.projects().serviceAccounts().keys(), 'create',
                   name=service_account['name'], body=key_body, retry_reasons=[404])
    oauth2service_data = base64.b64decode(key['privateKeyData'])
    write_file(service_account_file, oauth2service_data)
    print_text('Service account has been successfully created! ', stdscr)


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
    print_text('Credentials file has been successfully generated!')


def write_file(filename, data, stdscr=None, mode='wb'):
    if isinstance(data, str):
        data = data.encode('utf-8')
    try:
        with open(os.path.expanduser(filename), mode) as f:
            f.write(data)
        return True
    except IOError as error:
        print_text(error, stdscr)

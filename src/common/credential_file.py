import os
import sys


def generate_credentials_file(client_id, client_secret, project_id):
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
    write_file(client_secrets_file, cs_data, continue_of_error=True)


def write_file(filename, data, mode='wb', continue_of_error=False, display_error=True):
    if isinstance(data, str):
        data = data.encode('utf-8')
    try:
        with open(os.path.expanduser(filename), mode) as f:
            f.write(data)
        return True
    except IOError as e:
        if continue_of_error:
            if display_error:
                print(e)
            return False
        sys.exit()

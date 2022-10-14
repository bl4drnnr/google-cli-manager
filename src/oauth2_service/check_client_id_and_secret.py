import requests

from urllib.parse import urlencode


def check_client_id_and_secret(client_id, client_secret):
    error_msg = ''

    url = 'https://www.googleapis.com/oauth2/v4/token'
    post_data = {'client_id': client_id, 'client_secret': client_secret,
                 'code': 'ThisIsAnInvalidCodeOnlyBeingUsedToTestIfClientAndSecretAreValid',
                 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob', 'grant_type': 'authorization_code'}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    content = requests.post(url, urlencode(post_data), headers=headers)

    try:
        content = content.json()
    except ValueError:
        error_msg = 'Unknown error: %s' % content

    if 'error' not in content or 'error_description' not in content:
        error_msg = 'Unknown error: %s' % content
    if content['error'] == 'invalid_grant':
        return error_msg
    if content['error_description'] == 'The OAuth client was not found.':
        error_msg = '\nERROR!ERROR!ERROR!\n\nNot a valid client ID. Please make sure you are following the\n' \
                    'directions exactly and that there are no extra spaces in your client ID.'
        return error_msg
    if content['error_description'] == 'Unauthorized':
        error_msg = '\nERROR!ERROR!ERROR!\n\nNot a valid client secret. Please make sure you are following\n' \
                    'the directions exactly and that there are no extra spaces in your client secret.'
        return error_msg
    error_msg = 'Unknown error: %s' % content
    return error_msg

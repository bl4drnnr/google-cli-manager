import os
import sys

from src.exceptions.index import WrongOption, NoCredentialsFile

from src.api.services.email import email_backup
from src.api.services.drive import transfer_drive_ownership
from src.api.services.docs import transfer_documents_ownership
from src.api.services.calendar import transfer_calendar_events
from src.api.services.admin import suspend_user_activity
from src.api.services.admin import change_ou

from src.oauth2_service.check_client_id_and_secret import check_client_id_and_secret
from src.common.credential_file import generate_credentials_file


def cli_execute(operation, options):
    user_from = options['email_from']
    user_to = options['email_to']

    try:
        if not os.path.exists('credentials.json'):
            if 'client-id' not in options and 'client-secret' not in options and 'project-id' not in options:
                raise NoCredentialsFile
            else:
                client_id = input('Please, provide client ID: ')
                client_secret = input('Please, provide client secret: ')
                project_id = input('Please, provide project ID: ')

                valid_credentials_error = check_client_id_and_secret(client_id, client_secret)

                if len(valid_credentials_error) != 0:
                    print(valid_credentials_error)

                generate_credentials_file(client_id, client_secret, project_id)
                print('Credentials file has been generated!')

        if operation == 'offboard':
            suspend_user_activity(user_from)
            transfer_calendar_events(user_from, user_to)
            transfer_drive_ownership(user_from, user_to)
            email_backup(user_from, user_to)
            change_ou(user_from, '')
        elif operation == 'sua':
            suspend_user_activity(user_from)
        elif operation == 'tce':
            transfer_calendar_events(user_from, user_to)
        elif operation == 'tdo':
            transfer_drive_ownership(user_from, user_to)
        elif operation == 'cebl':
            email_backup(user_from, user_to)
        elif operation == 'cebg':
            email_backup(user_from, user_to)
        elif operation == 'tgdo':
            transfer_documents_ownership(user_from, user_to)
        else:
            raise WrongOption
    except WrongOption:
        print('Wrong option!')
        sys.exit()
    except NoCredentialsFile:
        print('No credentials were set!')
        print('Please, check manual with documentation ("-h" or "--help") in order to set them.')
        sys.exit()

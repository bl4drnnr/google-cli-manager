import os
import sys

from src.exceptions.index import WrongOption, NoCredentialsFile, NoOrganizationalUnitSet

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
                valid_credentials_error = check_client_id_and_secret(options['client-id'], options['client-secret'])

                if len(valid_credentials_error) != 0:
                    print(valid_credentials_error)

                generate_credentials_file(options['client-id'], options['client-secret'], options['project-id'])
                print('Credentials file has been generated!')

        if operation == 'offboard':
            if 'org-unit' not in options:
                raise NoOrganizationalUnitSet
            suspend_user_activity(user_from)
            change_ou(user_from, options['org-unit'])
            transfer_calendar_events(user_from, user_to)
            transfer_drive_ownership(user_from, user_to)
            transfer_documents_ownership(user_from, user_to)
            email_backup(user_from, user_to)
        elif operation == 'sua':
            suspend_user_activity(user_from)
        elif operation == 'cou':
            if 'org-unit' not in options:
                raise NoOrganizationalUnitSet
            change_ou(user_from, options['org-unit'])
        elif operation == 'tce':
            transfer_calendar_events(user_from, user_to)
        elif operation == 'tdo':
            transfer_drive_ownership(user_from, user_to)
        elif operation == 'tgdo':
            transfer_documents_ownership(user_from, user_to)
        elif operation == 'cebl':
            email_backup(user_from, user_to)
        elif operation == 'cebg':
            email_backup(user_from, user_to)
        else:
            raise WrongOption
    except WrongOption:
        print('Wrong option!')
        sys.exit()
    except NoCredentialsFile:
        print('No credentials were set!')
        print('Please, check manual with documentation ("-h" or "--help") in order to set them.')
        sys.exit()
    except NoOrganizationalUnitSet:
        print('No organizational unit set!')
        sys.exit()

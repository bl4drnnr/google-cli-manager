import os
import sys

from src.exceptions.index import WrongOption, NoCredentialsFile, NoOrganizationalUnitSet, GroupWrongData

from src.api.services.email import email_backup_locally, email_backup_group
from src.api.services.drive import transfer_drive_ownership
from src.api.services.docs import transfer_documents_ownership
from src.api.services.calendar import transfer_calendar_events
from src.api.services.admin import suspend_user_activity
from src.api.services.admin import change_ou
from src.api.services.groups import create_groups

from src.oauth2_service.check_client_id_and_secret import check_client_id_and_secret
from src.common.credential_file import generate_credentials_file, generate_service_account


def initiate_credentials_files(options):
    if \
            'client_id' not in options and \
            'secret' not in options and \
            'project_id' not in options and \
            'delegate' not in options:
        raise NoCredentialsFile
    else:
        valid_credentials_error = check_client_id_and_secret(options['client_id'], options['secret'])

        if len(valid_credentials_error) != 0:
            print(valid_credentials_error)

        generate_credentials_file(options['client_id'], options['secret'], options['project_id'])
        generate_service_account(options['project_id'], options['delegate'])


def cli_execute(operation, options):
    try:
        if not os.path.exists('credentials.json') or not os.path.exists('service.json'):
            initiate_credentials_files(options)

        if operation == 'offboard':
            if 'org_unit' not in options:
                raise NoOrganizationalUnitSet

            user_from = options['email_from']
            user_to = options['email_to']
            admin_user = options['admin']

            suspend_user_activity(user_from, admin_user)
            change_ou(user_from, options['org_unit'], admin_user)
            transfer_calendar_events(user_from, user_to, admin_user)
            transfer_drive_ownership(user_from, user_to, admin_user)
            transfer_documents_ownership(user_from, user_to, admin_user)
            email_backup_group(user_from, user_to, admin_user)
        elif operation == 'sua':
            suspend_user_activity(options['email_from'], options['admin'])
        elif operation == 'cou':
            if 'org_unit' not in options:
                raise NoOrganizationalUnitSet

            change_ou(options['email_from'], options['org_unit'], options['admin'])
        elif operation == 'tce':
            transfer_calendar_events(options['email_from'], options['email_to'], options['admin'])
        elif operation == 'tdo':
            transfer_drive_ownership(options['email_from'], options['email_to'], options['admin'])
        elif operation == 'tgdo':
            transfer_documents_ownership(options['email_from'], options['email_to'], options['admin'])
        elif operation == 'cebl':
            email_backup_locally(options['email_from'], options['admin'])
        elif operation == 'cebg':
            email_backup_group(options['email_from'], options['admin'])
        elif operation == 'cg':
            if 'group' not in options and 'admin' not in options and 'customer_id' not in options:
                raise GroupWrongData

            create_groups(options['group'], options['admin'], options['customer_id'])
        elif operation == 'init_cred':
            initiate_credentials_files(options)
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
    except GroupWrongData:
        print('In order to create Google Groups, please set all needed values.')
        sys.exit()

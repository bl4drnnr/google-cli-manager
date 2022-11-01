import os
import sys

from src.exceptions.index import WrongOption, NoCredentialsFile, WrongAttributes

from src.api.services.email import email_backup_locally, email_backup_group
from src.api.services.drive import transfer_drive_ownership
from src.api.services.docs import transfer_documents_ownership
from src.api.services.calendar import transfer_calendar_events
from src.api.services.groups import create_groups
from src.api.services.admin import \
    archive_user, \
    get_user_by_email, \
    suspend_user_activity, \
    change_ou

from src.oauth2_service.check_client_id_and_secret import check_client_id_and_secret
from src.common.credential_file import generate_credentials_file, generate_service_account


required_options = []


def check_required_options(set_options):
    if len(set_options) == 0:
        raise WrongAttributes

    for option in set_options:
        if option not in required_options:
            raise WrongAttributes


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
        credentials_files_generated = False

        if not os.path.exists('credentials.json') or not os.path.exists('service.json'):
            initiate_credentials_files(options)
            credentials_files_generated = True

        global required_options

        if operation == 'offboard':
            required_options = ['email_from', 'email_to', 'admin', 'org_unit', 'customer_id', 'users']
            check_required_options(options)

            user_from = options['email_from']
            user_to = options['email_to']
            admin_user = options['admin']
            org_unit = options['org_unit']
            customer_id = options['customer_id']
            users = options['users'].split(',')

            suspend_user_activity(user_from)
            change_ou(user_from, org_unit)
            transfer_calendar_events(user_from, user_to, admin_user)
            transfer_drive_ownership(user_from, user_to, admin_user)
            transfer_documents_ownership(user_from, user_to, admin_user)
            email_backup_group(user_from, admin_user, customer_id, users)
        elif operation == 'sua':
            required_options = ['email_from']
            check_required_options(options)

            suspend_user_activity(options['email_from'])
        elif operation == 'aua':
            required_options = ['email_from']
            check_required_options(options)

            archive_user(options['email_from'])
        elif operation == 'cou':
            required_options = ['email_from', 'org_unit']
            check_required_options(options)

            change_ou(options['email_from'], options['org_unit'])
        elif operation == 'tce':
            required_options = ['email_from', 'email_to', 'admin']
            check_required_options(options)

            transfer_calendar_events(options['email_from'], options['email_to'], options['admin'])
        elif operation == 'tdo':
            required_options = ['email_from', 'email_to', 'admin']
            check_required_options(options)

            transfer_drive_ownership(options['email_from'], options['email_to'], options['admin'])
        elif operation == 'tgdo':
            required_options = ['email_from', 'email_to', 'admin']
            check_required_options(options)

            transfer_documents_ownership(options['email_from'], options['email_to'], options['admin'])
        elif operation == 'cebl':
            required_options = ['email_from']
            check_required_options(options)

            email_backup_locally(options['email_from'])
        elif operation == 'cebg':
            required_options = ['email_from', 'admin', 'customer_id', 'users']
            check_required_options(options)
            users = options['users'].split(',')

            email_backup_group(options['email_from'], options['admin'], options['customer_id'], users)
        elif operation == 'cg':
            required_options = ['group', 'admin', 'customer_id']
            check_required_options(options)

            create_groups(options['group'], options['admin'], options['customer_id'])
        elif operation == 'init_cred' and not credentials_files_generated:
            initiate_credentials_files(options)
        elif operation == 'get_user':
            required_options = ['email_from']
            check_required_options(options)

            get_user_by_email(options['email_from'])
        else:
            if operation != 'init_cred':
                raise WrongOption
    except WrongOption:
        print('Wrong option!')
        sys.exit()
    except NoCredentialsFile:
        print('No credentials were set!')
        print('Please, check manual with documentation ("-h" or "--help") in order to set them.')
        sys.exit()
    except WrongAttributes:
        print(f'Wrong attributes, please, make sure you have set next attributes: {required_options}')
        sys.exit()

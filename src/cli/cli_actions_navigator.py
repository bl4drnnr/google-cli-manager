import os
import sys
import argparse

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

from src.common.functions import check_client_id_and_secret
from src.common.credential_file import generate_credentials_file, generate_service_account


required_options = []


class CliExecutor:
    def __init__(self, operation, options):
        self._operation = operation
        self._options = options

    def cli_execute(self):
        def check_required_options(set_options):
            if len(set_options) == 0:
                raise WrongAttributes

            for option in set_options:
                if option not in required_options and f"{option}/optional" not in required_options:
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

        try:
            credentials_files_generated = False

            if not os.path.exists('credentials.json') or not os.path.exists('service.json'):
                initiate_credentials_files(self._options)
                credentials_files_generated = True

            global required_options

            if self._operation == 'offboard':
                required_options = ['email_from', 'email_to', 'admin', 'org_unit', 'customer_id', 'users', 'backup_group/optional']
                check_required_options(self._options)

                user_from = self._options['email_from']
                user_to = self._options['email_to']
                admin_user = self._options['admin']
                org_unit = self._options['org_unit']
                customer_id = self._options['customer_id']
                users = self._options['users'].split(',')

                backup_group_name = self._options['backup_group'] if \
                    'backup_group' in self._options else \
                    user_from.split('@')[0] + '.backup@' + user_from.split('@')[1]

                suspend_user_activity(user_from)
                change_ou(user_from, org_unit)
                transfer_calendar_events(user_from, user_to, admin_user)
                transfer_drive_ownership(user_from, user_to, admin_user)
                transfer_documents_ownership(user_from, user_to, admin_user)
                email_backup_group(user_from, admin_user, customer_id, backup_group_name, users)
            elif self._operation == 'sua':
                required_options = ['email_from']
                check_required_options(self._options)

                suspend_user_activity(self._options['email_from'])
            elif self._operation == 'aua':
                required_options = ['email_from']
                check_required_options(self._options)

                archive_user(self._options['email_from'])
            elif self._operation == 'cou':
                required_options = ['email_from', 'org_unit']
                check_required_options(self._options)

                change_ou(self._options['email_from'], self._options['org_unit'])
            elif self._operation == 'tce':
                required_options = ['email_from', 'email_to', 'admin']
                check_required_options(self._options)

                transfer_calendar_events(self._options['email_from'], self._options['email_to'], self._options['admin'])
            elif self._operation == 'tdo':
                required_options = ['email_from', 'email_to', 'admin']
                check_required_options(self._options)

                transfer_drive_ownership(self._options['email_from'], self._options['email_to'], self._options['admin'])
            elif self._operation == 'tgdo':
                required_options = ['email_from', 'email_to', 'admin']
                check_required_options(self._options)

                transfer_documents_ownership(self._options['email_from'], self._options['email_to'], self._options['admin'])
            elif self._operation == 'cebl':
                required_options = ['email_from']
                check_required_options(self._options)

                email_backup_locally(self._options['email_from'])
            elif self._operation == 'cebg':
                required_options = ['email_from', 'admin', 'customer_id', 'users', 'backup_group/optional']
                check_required_options(self._options)
                users = self._options['users'].split(',')

                email_from = self._options['email_from']
                backup_group_name = self._options['backup_group'] if \
                    'backup_group' in self._options else \
                    email_from.split('@')[0] + '.backup@' + email_from.split('@')[1]

                email_backup_group(email_from, self._options['admin'], self._options['customer_id'], backup_group_name, users)
            elif self._operation == 'cg':
                required_options = ['group', 'admin', 'customer_id', 'backup_group/optional']
                check_required_options(self._options)

                create_groups(self._options['group'], self._options['admin'], self._options['customer_id'])
            elif self._operation == 'init_cred' and not credentials_files_generated:
                initiate_credentials_files(self._options)
            elif self._operation == 'get_user':
                required_options = ['email_from']
                check_required_options(self._options)

                get_user_by_email(self._options['email_from'])
            else:
                if self._operation != 'init_cred':
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

    @staticmethod
    def setup_available_options(argv):
        parser = argparse.ArgumentParser(add_help=False)
        first_execution = parser.add_argument_group('First execution credentials')
        services = parser.add_argument_group('Service')

        parser.add_argument('-h', '--help',
                            action='help',
                            help='Display this message.')

        parser.add_argument('-f', '--email-from',
                            metavar='',
                            help='Email of data sender user (offboarded user).')
        parser.add_argument('-t', '--email-to',
                            metavar='',
                            help='Email of data transfer receiver.')
        parser.add_argument('-a', '--admin',
                            metavar='',
                            help='Admin email. Used to use Service Account.')
        parser.add_argument('-g', '--group',
                            metavar='',
                            help='Name of the group.')
        parser.add_argument('-b', '--backup-group',
                            metavar='',
                            help='Name of the backup group. Default: *.backup@*')
        parser.add_argument('-o', '--org-unit',
                            metavar='',
                            help='Used for Google Admin Workspace organizational unit.')
        parser.add_argument('-r', '--customer-id',
                            metavar='',
                            help='In order to obtain Customer ID see README docs.')
        parser.add_argument('-u', '--users',
                            metavar='',
                            help='List of users. who has access to group in next format: user1@domain.com,user2@domain.com')

        parser.add_argument('--offboard',
                            help='General user offboard. See docs to know what is triggered.',
                            action='store_true')
        parser.add_argument('--sua',
                            help='Suspend user activity.',
                            action='store_true')
        parser.add_argument('--aua',
                            help='Archive user account.',
                            action='store_true')
        parser.add_argument('--cou',
                            help='Change user organizational unit.',
                            action='store_true')
        parser.add_argument('--tdo',
                            help='Transfer Google Drive ownership.',
                            action='store_true')
        parser.add_argument('--tce',
                            help='Transfer Google Calendar events.',
                            action='store_true')
        parser.add_argument('--tgdo',
                            help='Transfer Google Docs ownership',
                            action='store_true')
        parser.add_argument('--cebl',
                            help='Create email backup (locally).',
                            action='store_true')
        parser.add_argument('--cebg',
                            help='Create email backup (upload to Google Groups)',
                            action='store_true')
        parser.add_argument('--cg',
                            help='Create Google Group (use "-g" or "--group" in order to set group name)',
                            action='store_true')
        parser.add_argument('--get-user',
                            help='Get and print information about user.',
                            action='store_true')

        first_execution.add_argument('-c', '--client-id',
                                     metavar='',
                                     help='OAuth 2.0 client ID.')
        first_execution.add_argument('-s', '--secret',
                                     metavar='',
                                     help='OAuth 2.0 client secret.')
        first_execution.add_argument('-p', '--project-id',
                                     metavar='',
                                     help='Used for Google Admin Workspace.')
        first_execution.add_argument('-d', '--delegate',
                                     metavar='',
                                     help='Email to delegate Google Service Account.')

        services.add_argument('-i', '--init-cred',
                              help='Init or reinit credentials.',
                              action='store_true')

        return parser.parse_args(argv)


import os
import curses

from src.common.credential_file import generate_credentials_file, generate_service_account
from src.common.functions import print_raw_input, print_logo

from src.interactive_cli.menu.docs import commands_docs
from src.oauth2_service.check_client_id_and_secret import check_client_id_and_secret

from src.api.services.email import email_backup_locally, email_backup_group
from src.api.services.drive import transfer_drive_ownership
from src.api.services.docs import transfer_documents_ownership
from src.api.services.calendar import transfer_calendar_events
from src.api.services.admin import suspend_user_activity, change_ou
from src.api.services.groups import create_groups


def initiate_credentials_files(stdscr):
    client_id = print_raw_input(stdscr, 'Please, provide client ID: ')
    client_secret = print_raw_input(stdscr, 'Please, provide client secret: ')
    project_id = print_raw_input(stdscr, 'Please, provide project ID: ')
    admin_email = print_raw_input(stdscr, 'Provide email of delegated user: ')

    valid_credentials_error = check_client_id_and_secret(client_id, client_secret)

    generate_credentials_file(client_id, client_secret, project_id, stdscr)
    generate_service_account(project_id, admin_email, stdscr)

    if len(valid_credentials_error) != 0:
        stdscr.addstr(valid_credentials_error, curses.color_pair(3))
        stdscr.addstr('\n\nPress any key to get back...\n\n')
        stdscr.addstr('#################################', curses.A_BOLD)
        stdscr.getch()
        return


def command_execution(stdscr, command):
    print_logo(stdscr, 4)

    command_instructions = commands_docs[command]

    for idx, row in enumerate(command_instructions):
        if idx == 0:
            stdscr.addstr(f' - {row}', curses.A_BOLD)
        else:
            stdscr.addstr(row)

    if not os.path.exists('credentials.json') or not os.path.exists('service.json'):
        initiate_credentials_files(stdscr)

    if command == 'Offboard user':
        user_from = print_raw_input(stdscr, 'Please, provide email of offboarded user: ').strip()
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user (leave empty if no need): ').strip()
        org_unit = print_raw_input(stdscr, 'Provide Organizational Unit (leave empty if no need): ').strip()

        suspend_user_activity(user_from, admin_user, stdscr)
        change_ou(user_from, org_unit, admin_user, stdscr)
        transfer_calendar_events(user_from, user_to, admin_user, stdscr)
        transfer_drive_ownership(user_from, user_to, admin_user, stdscr)
        transfer_documents_ownership(user_from, user_to, admin_user, stdscr)
        email_backup_group(user_from, admin_user, stdscr)
    elif command == 'Suspend user activity':
        user_from = print_raw_input(stdscr, 'Please, provide email of account to suspend: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of admin or delegated user (leave empty if no need): ').strip()

        suspend_user_activity(user_from, admin_user, stdscr)
    elif command == 'Change user Organizational Unit':
        user_from = print_raw_input(stdscr, 'Please, provide email of account to change OU: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user (leave empty if no need): ').strip()
        org_unit = print_raw_input(stdscr, 'Provide Organizational Unit: ').strip()

        change_ou(user_from, org_unit, admin_user, stdscr)
    elif command == 'Transfer Google Drive ownership':
        user_from = print_raw_input(stdscr, 'Please, provide email of data sender: ').strip()
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user (leave empty if no need): ').strip()

        transfer_documents_ownership(user_from, user_to, admin_user, stdscr)
    elif command == 'Transfer Google Calendar events':
        user_from = print_raw_input(stdscr, 'Please, provide email of data sender: ').strip()
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user (leave empty if no need): ').strip()

        transfer_calendar_events(user_from, user_to, admin_user, stdscr)
    elif command == 'Transfer Google Docs ownership':
        user_from = print_raw_input(stdscr, 'Please, provide email of data sender: ').strip()
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user (leave empty if no need): ').strip()

        transfer_documents_ownership(user_from, user_to, admin_user, stdscr)
    elif command == 'Create Google Group':
        group_name = print_raw_input(stdscr, 'Please, provide the name of the group: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user: ').strip()
        customer_id = print_raw_input(stdscr, 'Provide customer ID: ').strip()

        create_groups(group_name, admin_user, customer_id, stdscr)
    elif command == 'Create email backup (locally)':
        backup_user = print_raw_input(stdscr, 'Please, provide email of user to backup: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user (leave empty if no need): ').strip()

        email_backup_locally(backup_user, admin_user, stdscr)
    elif command == 'Create email backup (upload to Google Groups)':
        backup_user = print_raw_input(stdscr, 'Please, provide email of user to backup: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user (leave empty if no need): ').strip()

        email_backup_group(backup_user, admin_user, stdscr)
    elif command == 'Initiate credentials files':
        initiate_credentials_files(stdscr)

    stdscr.addstr('\n\nPress any key to get back...\n\n')
    stdscr.addstr('#################################', curses.A_BOLD)
    stdscr.getch()

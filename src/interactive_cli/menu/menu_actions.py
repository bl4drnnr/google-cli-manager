import os
import curses

from src.common.credential_file import generate_credentials_file
from src.common.functions import print_raw_input, print_logo

from src.interactive_cli.menu.docs import commands_docs
from src.oauth2_service.check_client_id_and_secret import check_client_id_and_secret

from src.api.services.email import email_backup_locally, email_backup_group
from src.api.services.drive import transfer_drive_ownership
from src.api.services.docs import transfer_documents_ownership
from src.api.services.calendar import transfer_calendar_events
from src.api.services.admin import suspend_user_activity, change_ou


def command_execution(stdscr, command):
    print_logo(stdscr, 4)

    command_instructions = commands_docs[command]

    for idx, row in enumerate(command_instructions):
        if idx == 0:
            stdscr.addstr(f' - {row}', curses.A_BOLD)
        else:
            stdscr.addstr(row)

    if not os.path.exists('credentials.json'):
        client_id = print_raw_input(stdscr, 'Please, provide client ID: ')
        client_secret = print_raw_input(stdscr, 'Please, provide client secret: ')
        project_id = print_raw_input(stdscr, 'Please, provide project ID: ')

        valid_credentials_error = check_client_id_and_secret(client_id, client_secret)

        if len(valid_credentials_error) != 0:
            stdscr.addstr(valid_credentials_error, curses.color_pair(3))
            stdscr.addstr('\n\nPress any key to get back...\n\n')
            stdscr.addstr('#################################', curses.A_BOLD)
            stdscr.getch()
            return

        generate_credentials_file(client_id, client_secret, project_id, stdscr)

    user_from = print_raw_input(stdscr, 'Please, provide email of data sender: ').strip()
    admin_user = print_raw_input(stdscr, 'Provide email of admin or delegated user (leave empty if no need): ').strip()
    if command == 'Offboard user':
        org_unit = print_raw_input(stdscr, 'Provide Organizational Unit (leave empty if no need): ').strip()
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()

        suspend_user_activity(user_from, admin_user, stdscr)
        change_ou(user_from, org_unit, admin_user, stdscr)
        transfer_calendar_events(user_from, user_to, admin_user, stdscr)
        transfer_drive_ownership(user_from, user_to, admin_user, stdscr)
        transfer_documents_ownership(user_from, user_to, admin_user, stdscr)
        email_backup_group(user_from, user_to, admin_user, stdscr)
    elif command == 'Suspend user activity':
        suspend_user_activity(user_from, admin_user, stdscr)
    elif command == 'Change user Organizational Unit':
        org_unit = print_raw_input(stdscr, 'Provide Organizational Unit (leave empty if no need): ').strip()

        change_ou(user_from, org_unit, admin_user, stdscr)
    elif command == 'Transfer Google Drive ownership':
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()

        transfer_documents_ownership(user_from, user_to, admin_user, stdscr)
    elif command == 'Transfer Google Calendar events':
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()

        transfer_calendar_events(user_from, user_to, admin_user, stdscr)
    elif command == 'Transfer Google Docs ownership':
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()

        transfer_documents_ownership(user_from, user_to, admin_user, stdscr)
    elif command == 'Create email backup (locally)':
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()

        email_backup_locally(user_from, user_to, admin_user, stdscr)
    elif command == 'Create email backup (upload to Google Groups)':
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()

        email_backup_group(user_from, user_to, admin_user, stdscr)

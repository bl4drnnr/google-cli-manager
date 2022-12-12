import os
import curses

from src.common.credential_file import generate_credentials_file, generate_service_account
from src.common.functions import print_raw_input, print_logo, check_client_id_and_secret

from src.api.services.email import email_backup_locally, email_backup_group
from src.api.services.drive import transfer_drive_ownership
from src.api.services.docs import transfer_documents_ownership
from src.api.services.calendar import transfer_calendar_events
from src.api.services.admin import suspend_user_activity, change_ou, get_user_by_email, archive_user
from src.api.services.groups import create_groups

from src.common.functions import pad_refresh

from src.common.variables import PAD_HEIGHT, COMMAND_DOCS


def initiate_credentials_files(stdscr):
    client_id = print_raw_input(stdscr, 'Please, provide client ID: ')
    client_secret = print_raw_input(stdscr, 'Please, provide client secret: ')
    project_id = print_raw_input(stdscr, 'Please, provide project ID: ')
    admin_email = print_raw_input(stdscr, 'Provide email of delegated user: ')

    valid_credentials_error = check_client_id_and_secret(client_id, client_secret)

    if len(valid_credentials_error) != 0:
        stdscr.addstr(valid_credentials_error, curses.color_pair(3))
        stdscr.addstr('\n\nPress any key to get back...\n\n')
        stdscr.addstr('#################################', curses.A_BOLD)
        stdscr.getch()
        return 0
    else:
        height, width = stdscr.getmaxyx()
        y = 0
        current_row_idx = 0
        pad = curses.newpad(PAD_HEIGHT, width)

        generate_credentials_file(client_id, client_secret, project_id, pad, y, height, width)
        generate_service_account(project_id, admin_email, pad, y, height, width)

        while True:
            key = stdscr.getch()

            if key == ord('q') or key == ord('Q'):
                return 0

            if key == curses.KEY_UP and current_row_idx > 0:
                current_row_idx -= 1
            elif key == curses.KEY_DOWN:
                current_row_idx += 1

            pad_refresh(pad, current_row_idx, height, width)


def command_execution(stdscr, command):
    print_logo(stdscr, 4)

    command_instructions = COMMAND_DOCS[command]

    for idx, row in enumerate(command_instructions):
        if idx == 0:
            stdscr.addstr(f' - {row}', curses.A_BOLD)
        else:
            stdscr.addstr(row)

    credentials_files_generated = False
    result = None

    if not os.path.exists('credentials.json') or not os.path.exists('service.json'):
        result = initiate_credentials_files(stdscr)
        credentials_files_generated = True

    if result == 0:
        return

    if command == 'Offboard user':
        user_from = print_raw_input(stdscr, 'Please, provide email of offboarded user: ').strip()
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user (leave empty if no need): ').strip()
        org_unit = print_raw_input(stdscr, 'Provide Organizational Unit (leave empty if no need): ').strip()
        customer_id = print_raw_input(stdscr, 'Provide customer ID: ').strip()

        stdscr.addstr('Provide list users email in next format: user1@domain.com,user2@domain.com\n')
        users = print_raw_input(stdscr, 'Emails: ').strip().split(',')

        suspend_user_activity(user_from, stdscr)
        change_ou(user_from, org_unit, stdscr)
        transfer_calendar_events(user_from, user_to, admin_user, stdscr)
        transfer_drive_ownership(user_from, user_to, admin_user, stdscr)
        transfer_documents_ownership(user_from, user_to, admin_user, stdscr)
        email_backup_group(user_from, admin_user, customer_id, users, stdscr)
    elif command == 'Suspend user activity':
        user_from = print_raw_input(stdscr, 'Please, provide email of account to suspend: ').strip()

        suspend_user_activity(user_from, stdscr)
    elif command == 'Archive user':
        user_from = print_raw_input(stdscr, 'Please, provide email of account to suspend: ').strip()

        archive_user(user_from, stdscr)
    elif command == 'Change user Organizational Unit':
        user_from = print_raw_input(stdscr, 'Please, provide email of account to change OU: ').strip()
        org_unit = print_raw_input(stdscr, 'Provide Organizational Unit: ').strip()

        change_ou(user_from, org_unit, stdscr)
    elif command == 'Transfer Google Drive ownership':
        user_from = print_raw_input(stdscr, 'Please, provide email of data sender: ').strip()
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user: ').strip()

        transfer_drive_ownership(user_from, user_to, admin_user, stdscr)
    elif command == 'Transfer Google Calendar events':
        user_from = print_raw_input(stdscr, 'Please, provide email of data sender: ').strip()
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user: ').strip()

        transfer_calendar_events(user_from, user_to, admin_user, stdscr)
    elif command == 'Transfer Google Docs ownership':
        user_from = print_raw_input(stdscr, 'Please, provide email of data sender: ').strip()
        user_to = print_raw_input(stdscr, 'Please, provide email of data receiver: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user: ').strip()

        transfer_documents_ownership(user_from, user_to, admin_user, stdscr)
    elif command == 'Create Google Group':
        group_name = print_raw_input(stdscr, 'Please, provide the name of the group: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user: ').strip()
        customer_id = print_raw_input(stdscr, 'Provide customer ID: ').strip()

        create_groups(group_name, admin_user, customer_id, stdscr)
    elif command == 'Create email backup (locally)':
        backup_user = print_raw_input(stdscr, 'Please, provide email of user to backup: ').strip()

        email_backup_locally(backup_user, stdscr)
    elif command == 'Create email backup (upload to Google Groups)':
        backup_user = print_raw_input(stdscr, 'Please, provide email of user to backup: ').strip()
        admin_user = print_raw_input(stdscr, 'Provide email of delegated user: ').strip()
        customer_id = print_raw_input(stdscr, 'Provide customer ID: ').strip()

        stdscr.addstr('Provide list users email in next format: user1@domain.com,user2@domain.com\n')
        users = print_raw_input(stdscr, 'Emails: ').strip().split(',')

        email_backup_group(backup_user, admin_user, customer_id, stdscr)
    elif command == 'Get user by email':
        user_email = print_raw_input(stdscr, 'Please, provide email of user you want to get: ').strip()

        result = get_user_by_email(user_email, stdscr)
    elif command == 'Initiate credentials files' and not credentials_files_generated:
        result = initiate_credentials_files(stdscr)

    if result != 0:
        stdscr.addstr('\n\nPress Q to get back...\n\n')
        stdscr.addstr('#################################', curses.A_BOLD)
        while True:
            key = stdscr.getch()
            if key == ord('q') or key == ord('Q'):
                return
    else:
        return

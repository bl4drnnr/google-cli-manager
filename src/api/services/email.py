from src.api.service_initiator import init_service_account_object
from src.api.actions.email.create_email_backup_locally import create_email_backup
from src.api.actions.email.create_email_backup_groups import restore_group

from src.common.print_text import print_text


def email_backup_locally(email_from, email_to, delegated_user, stdscr=None):
    try:
        service = init_service_account_object('gmail', email_from, delegated_user)
        create_email_backup(email_from, service, stdscr)
    except Exception as e:
        error = f'An error occurred while creating locally email backup: {e}'
        print_text(error, stdscr, error=True)


def email_backup_group(email_from, email_to, delegated_user, stdscr=None):
    try:
        service = init_service_account_object('gmail', email_from, delegated_user)
        backup_items = create_email_backup(email_from, service, stdscr=stdscr, return_objects=True)
        # Create group here
        service = init_service_account_object('groupsmigration', email_from, delegated_user)
        restore_group(
            email_from,
            service,
            backup_items['local_folder'],
            backup_items['sqlcur'],
            backup_items['sqlconn'],
            stdscr
        )
        # Remove folder after
    except Exception as e:
        error = f'An error occurred while creating group email backup: {e}'
        print_text(error, stdscr, error=True)

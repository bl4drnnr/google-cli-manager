import shutil

from src.api.service_initiator import init_service_account_object
from src.api.actions.email.create_email_backup_locally import create_email_backup
from src.api.actions.email.create_email_backup_groups import restore_group

from src.api.services.groups import create_groups

from src.common.print_text import print_text


def email_backup_locally(email_from, delegated_user, stdscr=None):
    try:
        service = init_service_account_object('gmail', email_from, delegated_user)
        create_email_backup(email_from, service, stdscr=stdscr, return_objects=False)
    except Exception as e:
        error = f'An error occurred while creating locally email backup: {e}'
        print_text(error, stdscr, error=True)


def email_backup_group(email_from, delegated_user, customer_id, stdscr=None):
    try:
        service = init_service_account_object('gmail', email_from, delegated_user)
        backup_items = create_email_backup(email_from, service, stdscr=stdscr, return_objects=True)

        backup_group_name = email_from.split('@')[0] + 'backup@' + email_from.split('@')[1]
        create_groups(backup_group_name, delegated_user, customer_id, stdscr)

        service = init_service_account_object('groupsmigration', email_from, delegated_user)
        restore_group(
            email_from,
            service,
            backup_items['local_folder'],
            backup_items['sqlcur'],
            backup_items['sqlconn'],
            stdscr
        )

        shutil.rmtree(f'gmcli-gmail-backup-{email_from}')
    except Exception as e:
        error = f'An error occurred while creating group email backup: {e}'
        print_text(error, stdscr, error=True)

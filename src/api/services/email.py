import shutil

from src.api.service_initiator import ServiceInitiator
from src.api.actions.email.create_email_backup_locally import create_email_backup
from src.api.actions.email.create_email_backup_groups import restore_group

from src.api.services.groups import create_groups, gain_group_access

from src.common.functions import print_text


def email_backup_locally(email_from, stdscr=None):
    try:
        service_initiator = ServiceInitiator('gmail')
        service = service_initiator.init_service_account_object(email_from, None)
        create_email_backup(email_from, service, stdscr=stdscr, return_objects=False)
    except Exception as e:
        error = f'An error occurred while creating locally email backup: {e}'
        print_text(error, stdscr, error=True)


def email_backup_group(email_from, delegated_user, customer_id, backup_group_name, users, stdscr=None):
    try:
        service_initiator = ServiceInitiator('gmail')
        service = service_initiator.init_service_account_object(email_from, None)
        backup_items = create_email_backup(email_from, service, stdscr=stdscr, return_objects=True)

        create_groups(backup_group_name, delegated_user, customer_id, stdscr)
        gain_group_access(backup_group_name, users, stdscr)

        service_initiator = ServiceInitiator('groupsmigration')
        service = service_initiator.init_service_account_object(email_from, delegated_user)
        restore_group(
            email_from,
            service,
            backup_group_name,
            backup_items['local_folder'],
            backup_items['sqlcur'],
            backup_items['sqlconn'],
            stdscr
        )

        shutil.rmtree(f'gmcli-gmail-backup-{email_from}')
    except Exception as e:
        error = f'An error occurred while creating group email backup: {e}'
        print_text(error, stdscr, error=True)

from src.api.service_initiator import init_services
from src.api.actions.email.create_email_backup import create_email_backup

from src.common.error_handler import print_error


def email_backup(email_from, email_to, stdscr=None):
    try:
        service = init_services('gmail', 'v1', email_to)
        create_email_backup(email_from, email_to, service)
    except Exception as e:
        error = f'An error occurred while creating email backup: {e}'
        print_error(error, stdscr)

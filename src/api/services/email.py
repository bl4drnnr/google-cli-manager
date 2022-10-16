from src.api.service_initiator import init_services
from src.api.actions.email.create_email_backup import create_email_backup

from src.common.print_text import print_text


def email_backup(email_from, email_to, delegated_user, stdscr=None):
    try:
        service = init_services('gmail', 'v1', delegated_user)
        create_email_backup(email_from, email_to, service, stdscr)
    except Exception as e:
        error = f'An error occurred while creating email backup: {e}'
        print_text(error, stdscr, error=True)

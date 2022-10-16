from src.api.service_initiator import init_services
from src.api.actions.drive.transfer_ownership import transfer_ownership

from src.common.print_text import print_text


def transfer_drive_ownership(email_from, email_to, stdscr=None):
    try:
        service = init_services('drive', 'v3')
        transfer_ownership(email_from, email_to, service, stdscr)
    except Exception as e:
        error = f'An error occurred while transferring drive ownership: {e}'
        print_text(error, stdscr, error=True)

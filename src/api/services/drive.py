from src.api.service_initiator import init_services
from src.api.actions.drive.transfer_ownership import transfer_ownership

from src.common.error_handler import print_error


def transfer_drive_ownership(email_from, email_to, stdscr=None):
    try:
        service = init_services('drive', 'v3')
        transfer_ownership(email_from, email_to, service)
    except Exception as e:
        error = f'An error occurred while transferring drive ownership: {e}'
        print_error(error, stdscr)

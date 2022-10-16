from src.api.service_initiator import init_services
from src.api.actions.docs.tranfer_ownership import transfer_ownership

from src.common.error_handler import print_error


def transfer_documents_ownership(email_from, email_to, stdscr=None):
    try:
        service = init_services('docs', 'v1')
        transfer_ownership(email_from, email_to, service)
    except Exception as e:
        error = f'An error occurred while transferring document ownership: {e}'
        print_error(error, stdscr)

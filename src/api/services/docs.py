from src.api.service_initiator import init_services
from src.api.actions.docs.tranfer_ownership import transfer_ownership

from src.common.print_text import print_text


def transfer_documents_ownership(email_from, email_to, delegated_user, stdscr=None):
    try:
        service = init_services('docs', 'v1', delegated_user)
        transfer_ownership(email_from, email_to, service, stdscr)
    except Exception as e:
        error = f'An error occurred while transferring document ownership: {e}'
        print_text(error, stdscr, error=True)

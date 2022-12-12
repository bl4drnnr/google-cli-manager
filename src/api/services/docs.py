from src.api.service_initiator import ServiceInitiator
from src.api.actions.docs.tranfer_ownership import transfer_ownership

from src.common.functions import print_text


def transfer_documents_ownership(email_from, email_to, delegated_user, stdscr=None):
    try:
        service_initiator = ServiceInitiator('docs', delegated_user)
        service = service_initiator.init_services()
        transfer_ownership(email_from, email_to, service, stdscr)
    except Exception as e:
        error = f'An error occurred while transferring document ownership: {e}'
        print_text(error, stdscr, error=True)

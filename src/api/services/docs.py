from src.api.service_initiator import init_services

from src.api.actions.docs.tranfer_ownership import transfer_ownership


def transfer_documents_ownership(email_from, email_to):
    try:
        service = init_services('docs', 'v1')
        transfer_ownership(email_from, email_to, service)
    except Exception as e:
        print(f'An error occurred while transferring document ownership: {e}')

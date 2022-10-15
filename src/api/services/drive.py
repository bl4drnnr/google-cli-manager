from src.api.service_initiator import init_services

from src.api.actions.drive.transfer_ownership import transfer_ownership


def transfer_drive_ownership(email_from, email_to):
    try:
        service = init_services('drive', 'v3')
        transfer_ownership(email_from, email_to, service)
    except Exception as e:
        print(f'An error occurred while transferring drive ownership: {e}')

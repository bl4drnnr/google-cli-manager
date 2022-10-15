from src.api.service_initiator import init_services

from src.api.actions.email.create_email_backup import create_email_backup


def email_backup(email_from, email_to):
    try:
        service = init_services('gmail', 'v1', email_to)
        create_email_backup(email_from, email_to, service)
    except Exception as e:
        print(f'An error occurred while creating email backup: {e}')

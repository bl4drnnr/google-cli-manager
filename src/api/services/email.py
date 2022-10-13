from src.api.service_initiator import init_services

from src.api.actions.email.forward_email import forward_email


def enable_email_forwarding(email_from, email_to, file_name):
    try:
        service = init_services(file_name, 'gmail', 'v1', email_to)
        forward_email(email_from, email_to, service)
    except Exception as e:
        print(f'An error occurred: {e}')

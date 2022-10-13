from src.api.service_initiator import init_services

from src.api.actions.admin.suspend_user_activity import suspend_user


def suspend_user_activity(email, file_name):
    try:
        service = init_services(file_name, 'admin', 'directory_v1')
        suspend_user(email, service)
    except Exception as e:
        print(f'An error occurred: {e}')

from src.api.service_initiator import init_services

from src.api.actions.admin.suspend_user_activity import suspend_user
from src.api.actions.admin.change_organizational_unit import change_organizational_unit


def suspend_user_activity(email, file_name):
    try:
        service = init_services(file_name, 'admin', 'directory_v1')
        suspend_user(email, service)
    except Exception as e:
        print(f'An error occurred while suspending user activity: {e}')


def change_ou(email, ou, file_name):
    try:
        service = init_services(file_name, 'admin', 'directory_v1')
        change_organizational_unit(email, service, ou)
    except Exception as e:
        print(f'An error occurred while changing organizational unit: {e}')

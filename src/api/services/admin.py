from src.api.service_initiator import init_services

from src.api.actions.admin.suspend_user_activity import suspend_user
from src.api.actions.admin.change_organizational_unit import change_organizational_unit

from src.common.print_text import print_text


def suspend_user_activity(email, stdscr=None):
    try:
        service = init_services('admin', 'directory_v1')
        suspend_user(email, service)
    except Exception as e:
        error = f'An error occurred while suspending user activity: {e}'
        print_text(error, stdscr, error=True)


def change_ou(email, ou, stdscr=None):
    try:
        service = init_services('admin', 'directory_v1')
        change_organizational_unit(email, service, ou)
    except Exception as e:
        error = f'An error occurred while changing organizational unit: {e}'
        print_text(error, stdscr, error=True)

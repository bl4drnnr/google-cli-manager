from src.api.service_initiator import init_services

from src.api.actions.admin.suspend_user_activity import suspend_user
from src.api.actions.admin.change_organizational_unit import change_organizational_unit
from src.api.actions.admin.get_user import get_user
from src.api.actions.admin.archive_user_account import archive_user_account

from src.common.functions import print_text


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
        change_organizational_unit(email, service, ou, stdscr)
    except Exception as e:
        error = f'An error occurred while changing organizational unit: {e}'
        print_text(error, stdscr, error=True)


def get_user_by_email(email, stdscr=None):
    try:
        service = init_services('admin', 'directory_v1', None)
        res = get_user(email, service, stdscr)
        return res
    except Exception as e:
        error = f'An error occurred while getting user: {e}'
        print_text(error, stdscr, error=True)
        return -1


def archive_user(email, stdscr=None):
    try:
        service = init_services('admin', 'directory_v1')
        archive_user_account(email, service, stdscr)
    except Exception as e:
        error = f'An error occurred while archiving user account: {e}'
        print_text(error, stdscr, error=True)

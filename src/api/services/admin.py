import curses

from src.api.service_initiator import init_services

from src.api.actions.admin.suspend_user_activity import suspend_user
from src.api.actions.admin.change_organizational_unit import change_organizational_unit


def suspend_user_activity(email, stdscr=None):
    try:
        service = init_services('admin', 'directory_v1')
        suspend_user(email, service)
    except Exception as e:
        error = f'An error occurred while suspending user activity: {e}'
        if stdscr is not None:
            stdscr.addstr(f'\n{error}', curses.A_BOLD | curses.color_pair(3))
        else:
            print(error)


def change_ou(email, ou, stdscr=None):
    try:
        service = init_services('admin', 'directory_v1')
        change_organizational_unit(email, service, ou)
    except Exception as e:
        error = f'An error occurred while changing organizational unit: {e}'
        if stdscr is not None:
            stdscr.addstr(f'\n{error}', curses.A_BOLD | curses.color_pair(3))
        else:
            print(error)

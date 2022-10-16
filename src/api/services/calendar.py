import curses

from src.api.service_initiator import init_services

from src.api.actions.calendar.merge_calendar import merge_calendar


def transfer_calendar_events(email_from, email_to, stdscr=None):
    try:
        service = init_services('calendar', 'v3', email_from)
        merge_calendar(email_from, email_to, service)
    except Exception as e:
        error = f'An error occurred while transferring calendar events: {e}'
        if stdscr is not None:
            stdscr.addstr(f'\n{error}', curses.A_BOLD | curses.color_pair(3))
        else:
            print(error)

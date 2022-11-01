from src.api.service_initiator import init_services
from src.api.actions.calendar.merge_calendar import transfer_events

from src.common.print_text import print_text


def transfer_calendar_events(email_from, email_to, delegated_user, stdscr=None):
    try:
        service = init_services('calendar', 'v3', delegated_user)
        transfer_events(email_from, email_to, service, stdscr)
    except Exception as e:
        error = f'An error occurred while transferring calendar events: {e}'
        print_text(error, stdscr, error=True)
